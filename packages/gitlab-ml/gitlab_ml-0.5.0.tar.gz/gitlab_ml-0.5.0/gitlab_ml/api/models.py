from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, unquote

import httpx
import mlflow
from mlflow.tracking import MlflowClient
from dateutil.parser import parse as parse_date
from gitlab.v4.objects import Project
from gitlab_ml.api.client import GitLabClient
from gitlab_ml.utils.logger import get_logger
from pydantic import BaseModel
from rich.progress import Progress
import os

logger = get_logger(__name__)


class ModelVersion(BaseModel):
    """Model version metadata."""
    version: str
    created_at: datetime
    author: str
    message: Optional[str] = None
    artifacts: List[str]


class Model(BaseModel):
    """Model metadata."""
    name: str
    versions: List[ModelVersion] = []

    @property
    def latest_version(self) -> Optional[str]:
        """Get the latest version."""
        if not self.versions:
            return None
        return self.versions[-1].version


class ModelRegistry:
    """Interface to GitLab's Model Registry using ML Model Package type."""
    
    def __init__(self, client: GitLabClient):
        """Initialize with GitLab client."""
        self.client = client
        self.project: Project = client.project
        
        # Configure MLflow with correct endpoint path
        project_path = quote(self.project.path_with_namespace, safe='')
        mlflow_uri = f"{self.client.client.url}/api/v4/projects/{project_path}/ml/mlflow"
        logger.debug(f"Setting MLflow tracking URI: {mlflow_uri}")
        
        mlflow.set_tracking_uri(mlflow_uri)
        os.environ["MLFLOW_TRACKING_TOKEN"] = self.client.client.private_token
        self.mlflow_client = MlflowClient()
    
    def _graphql_query(self, query: str, variables: Optional[Dict] = None) -> dict:
        """Execute a GraphQL query against GitLab API."""
        url = f"{self.client.client.url}/api/graphql"
        headers = {
            "Authorization": f"Bearer {self.client.client.private_token}",
            "Content-Type": "application/json",
        }
        
        try:
            response = httpx.post(
                url,
                headers=headers,
                json={"query": query, "variables": variables} if variables else {"query": query},
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                raise ValueError(f"GraphQL query failed: {result['errors']}")
            
            return result.get("data", {})
        except Exception as e:
            logger.error(f"GraphQL query failed: {e}")
            raise ValueError(f"Failed to execute GraphQL query: {e}")
    
    def _get_model_version_id(self, model_name: str, version: str) -> Tuple[str, str]:
        """Get project ID and model version ID using GraphQL."""
        query = """
        query GetMLModel($fullPath: ID!, $modelName: String!, $version: String!) {
            project(fullPath: $fullPath) {
                id
                mlModels(name: $modelName) {
                    nodes {
                        id
                        name
                        versions(version: $version) {
                            nodes {
                                id
                                version
                                packageId
                            }
                        }
                    }
                }
            }
        }
        """
        
        try:
            response = self._graphql_query(query, variables={
                "fullPath": self.project.path_with_namespace, 
                "modelName": model_name,
                "version": version
            })
            project_id = response['project']['id'].split('/')[-1]
            model_version_id = response['project']['mlModels']['nodes'][0]['versions']['nodes'][0]['id'].split('/')[-1]
            packageId = response['project']['mlModels']['nodes'][0]['versions']['nodes'][0]['packageId']
            return project_id, model_version_id, packageId
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to get model version ID: {e}")
            raise ValueError(f"Model {model_name} version {version} not found")
    
    def _get_package_name(self, model_name: str) -> str:
        """Get package name for a model."""
        return model_name  # No need for prefix with ML Model package type
    
    def _encode_file_path(self, path: str) -> str:
        """Encode file path for GitLab API.
        Preserves forward slashes for path structure but encodes other special characters."""
        # Split path by forward slashes and encode each part separately
        parts = path.split('/')
        encoded_parts = [quote(part, safe='') for part in parts]
        # Join with forward slashes
        return '/'.join(encoded_parts)
    
    def _decode_file_path(self, path: str) -> str:
        """Decode file path from GitLab API.
        Handles paths with encoded characters while preserving structure."""
        # Split by forward slashes and decode each part
        parts = path.split('/')
        decoded_parts = [unquote(part) for part in parts]
        # Join with forward slashes
        return '/'.join(decoded_parts)
    
    def list_models(
        self,
        author: Optional[str] = None,
    ) -> List[Model]:
        """List all models in the registry."""
        try:
            # Get all packages with pagination, filtering for ML models
            packages = self.project.packages.list(package_type='ml_model', all=True)
            models_dict = {}
            
            for package_ref in packages:
                # Get full package data
                package = self.project.packages.get(package_ref.id)
                
                # Get package metadata
                try:
                    package_meta = package._attrs  # Access raw package data
                    package_author = package_meta.get('_links', {}).get('creator', 'unknown')
                    if isinstance(package_author, dict):
                        package_author = package_author.get('username', 'unknown')
                    elif '/' in package_author:
                        package_author = package_author.split('/')[-1]
                except Exception:
                    package_author = 'unknown'
                
                # Skip if author filter doesn't match
                if author and package_author != author:
                    continue
                
                # Create or update model entry
                model_name = package.name
                if model_name not in models_dict:
                    models_dict[model_name] = Model(name=model_name)
                
                # Add version if it's not the metadata version
                if package.version != "0.0.0":
                    # Get all package files with pagination
                    package_files = package.package_files.list(all=True)
                    version = ModelVersion(
                        version=package.version,
                        created_at=parse_date(package.created_at),
                        author=package_author,
                        message=package.version,  # Use version as message since description isn't available
                        artifacts=[f.file_name for f in package_files],
                    )
                    models_dict[model_name].versions.append(version)
            
            # Sort versions by creation time
            for model in models_dict.values():
                model.versions.sort(key=lambda v: v.created_at)
            
            return list(models_dict.values())
            
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise ValueError(f"Failed to list models: {e}")
    
    def create_model(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Model:
        """Create a new model in the registry."""
        try:
            # Create model in MLflow
            try:
                mlflow_model = self.mlflow_client.create_registered_model(
                    name=name,
                    description=description or ""
                )
                logger.debug(f"Created MLflow model: {mlflow_model}")
            except Exception as e:
                if "RESOURCE_ALREADY_EXISTS" in str(e):
                    raise ValueError(f"Model '{name}' already exists")
                logger.error(f"MLflow model creation failed: {e}")
                raise ValueError(f"Failed to create model: {str(e).split(':')[0]}")
            
            # Create model metadata
            model = Model(
                name=name,
                versions=[]
            )
            
            return model
            
        except ValueError as e:
            # Re-raise ValueError with clean message
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Failed to create model: {e}")
            raise ValueError("An unexpected error occurred while creating the model")
    
    def upload_version(
        self,
        model_name: str,
        version: str,
        path: Path,
        message: Optional[str] = None,
    ) -> ModelVersion:
        """Upload a new version of a model."""
        artifacts = []
        chunk_size = 8192  # 8KB chunks for better memory management
        
        try:
            # Create version in MLflow first
            try:
                # Use source="/" since we're not using MLflow's artifact store
                mlflow_version = self.mlflow_client.create_model_version(
                    model_name,
                    version,
                    description=message or "",
                    tags={"gitlab.version": version}
                )
                logger.debug(f"Created MLflow version: {mlflow_version}")
            except Exception as e:
                logger.error(f"MLflow version creation failed: {e}")
                # Continue with GitLab upload even if MLflow fails
                pass
            
            # Get project ID and model version ID
            project_id, model_version_id, packageId = self._get_model_version_id(model_name, version)
            
            # Upload files with progress bar
            with Progress() as progress:
                if path.is_dir():
                    # Get list of all files and calculate total size
                    files = [f for f in path.rglob('*') if f.is_file()]
                    total_size = sum(f.stat().st_size for f in files)
                    
                    # Create overall progress bar
                    overall_task = progress.add_task(
                        f"Uploading directory '{path.name}'...",
                        total=len(files)
                    )
                    
                    # Upload each file individually
                    for file in files:
                        # Skip __pycache__ files
                        if '__pycache__' in str(file):
                            progress.update(overall_task, advance=1)
                            continue

                        # Get relative path to preserve directory structure
                        relative_path = file.relative_to(path)
                        artifact_name = str(relative_path)
                        
                        # Create file progress bar
                        file_task = progress.add_task(
                            f"Uploading {artifact_name}...",
                            total=file.stat().st_size,
                            visible=True
                        )
                        
                        # Create upload URL using model version ID
                        upload_url = (
                            f"{self.client.client.url}/api/v4/projects/{project_id}/"
                            f"packages/ml_models/{model_version_id}/files/{artifact_name}"
                        )
                        
                        headers = {"Authorization": f"Bearer {self.client.client.private_token}"}
                        
                        logger.debug(f"Uploading to URL: {upload_url}")
                        
                        # Stream upload in chunks
                        with open(file, 'rb') as f:
                            uploaded_size = 0
                            while True:
                                chunk = f.read(chunk_size)
                                if not chunk:
                                    break
                                    
                                # Upload chunk
                                response = httpx.put(
                                    upload_url,
                                    headers=headers,
                                    content=chunk,
                                    timeout=None
                                )
                                response.raise_for_status()
                                
                                uploaded_size += len(chunk)
                                progress.update(file_task, completed=uploaded_size)
                        
                        artifacts.append(artifact_name)
                        progress.update(overall_task, advance=1)
                        progress.remove_task(file_task)
                else:
                    # Single file upload
                    artifact_name = path.name
                    file_task = progress.add_task(
                        f"Uploading {artifact_name}...",
                        total=path.stat().st_size
                    )
                    
                    # Create upload URL using model version ID
                    upload_url = (
                        f"{self.client.client.url}/api/v4/projects/{project_id}/"
                        f"packages/ml_models/{model_version_id}/files/{artifact_name}"
                    )
                    
                    headers = {"Authorization": f"Bearer {self.client.client.private_token}"}
                    
                    logger.debug(f"Uploading to URL: {upload_url}")
                    
                    # Stream upload in chunks
                    with open(path, 'rb') as f:
                        uploaded_size = 0
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                                
                            # Upload chunk
                            response = httpx.put(
                                upload_url,
                                headers=headers,
                                content=chunk,
                                timeout=None
                            )
                            response.raise_for_status()
                            
                            uploaded_size += len(chunk)
                            progress.update(file_task, completed=uploaded_size)
                    
                    artifacts.append(artifact_name)
            
            # Create version metadata
            version_metadata = ModelVersion(
                version=version,
                created_at=datetime.utcnow(),
                author=self.client.client.user.username,
                message=message,
                artifacts=artifacts,
            )
            
            return version_metadata
            
        except Exception as e:
            logger.error(f"Failed to upload version: {e}")
            raise ValueError(f"Failed to upload version {version} of model {model_name}: {e}")
    
    def download_version(
        self,
        model_name: str,
        version: str,
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Download a specific version of a model."""
        output_dir = output_dir or Path.cwd()
        output_dir = Path(output_dir)
        output_dir = output_dir / model_name / version
        output_dir.mkdir(parents=True, exist_ok=True)
        chunk_size = 8192  # 8KB chunks for better memory management
        
        try:
            # Get project ID, model version ID and package ID
            project_id, model_version_id, package_id = self._get_model_version_id(model_name, version)
            
            # Get files using GraphQL
            files = self._get_package_files_graphql(package_id)
            
            if not files:
                raise ValueError("No files found in package")
            
            # Download each file
            downloaded_paths = []
            with Progress() as progress:
                overall_task = progress.add_task(
                    f"Downloading {model_name} {version}...",
                    total=len(files)
                )
                
                for file in files:
                    try:
                        # Skip __pycache__ files
                        if '__pycache__' in file['fileName']:
                            progress.update(overall_task, advance=1)
                            continue
                            
                        # Get the original file name and decode any URL encoding
                        filename = unquote(file['fileName'])
                        file_path = output_dir / filename
                        
                        # Create parent directories if needed
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Create download URL - use decoded filename
                        download_url = (
                            f"{self.client.client.url}/api/v4/projects/{project_id}/"
                            f"packages/ml_models/{model_version_id}/files/{filename}"
                        )
                        
                        logger.debug(f"Downloading from URL: {download_url}")
                        
                        # Download with progress
                        file_task = progress.add_task(
                            f"Downloading {filename}...",
                            total=int(file['size'])
                        )
                        
                        headers = {"Authorization": f"Bearer {self.client.client.private_token}"}
                        
                        # Stream download in small chunks
                        with httpx.stream("GET", download_url, headers=headers, follow_redirects=True) as response:
                            response.raise_for_status()
                            
                            # Open file in binary write mode and stream chunks
                            with open(file_path, 'wb') as f:
                                downloaded_size = 0
                                for chunk in response.iter_bytes(chunk_size=chunk_size):
                                    if chunk:  # Filter out keep-alive chunks
                                        f.write(chunk)
                                        downloaded_size += len(chunk)
                                        progress.update(file_task, completed=downloaded_size)
                        
                        downloaded_paths.append(file_path)
                        progress.update(overall_task, advance=1)
                        progress.remove_task(file_task)
                            
                    except Exception as e:
                        logger.error(f"Failed to download {filename}: {e}")
                        # Clean up partially downloaded file
                        if file_path.exists():
                            file_path.unlink()
                        raise ValueError(f"Failed to download {filename}: {e}")
            
            # If we only downloaded one file, return its path
            # Otherwise return the directory
            if len(downloaded_paths) == 1:
                return downloaded_paths[0]
            return output_dir
            
        except Exception as e:
            logger.error(f"Failed to download version: {e}")
            raise ValueError(
                f"Failed to download version {version} of model {model_name}: {e}"
            )
    
    def delete_model(self, model_name: str, version: Optional[str] = None) -> None:
        """Delete a model or specific version from the registry.
        
        Args:
            model_name: Name of the model
            version: Optional version to delete. If None, deletes entire model
        """
        try:
            if version:
                # Delete specific version
                try:
                    project_id, model_version_id, package_id = self._get_model_version_id(model_name, version)
                    print(project_id, model_version_id, package_id)
                    self.mlflow_client.delete_model_version(name=model_name, version=model_version_id)
                    logger.debug(f"Deleted version {version} of model {model_name}")
                except Exception as e:
                    logger.error(f"Failed to delete version: {e}")
                    raise ValueError(f"Failed to delete version {version} of model {model_name}: {e}")
            else:
                # Delete entire model
                try:
                    self.mlflow_client.delete_registered_model(name=model_name)
                    logger.debug(f"Deleted model {model_name}")
                except ValueError:
                    raise
                except Exception as e:
                    logger.error(f"Failed to delete model: {e}")
                    raise ValueError(f"Failed to delete model '{model_name}': Unexpected error occurred")
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete: {e}")
            raise ValueError(f"Failed to delete: Unexpected error occurred")
    
    def _get_package_files_graphql(self, package_id: str) -> List[Dict]:
        """Get package files using GraphQL API."""
        query = """
        query getPackageFiles($id: PackagesPackageID!) {
          package(id: $id) {
            id
            packageFiles {
              nodes {
                id
                fileMd5
                fileName
                fileSha1
                fileSha256
                size
                createdAt
                downloadPath
              }
            }
          }
        }
        """
        
        try:
            response = self._graphql_query(query, variables={"id": package_id})
            return response["package"]["packageFiles"]["nodes"]
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to get package files: {e}")
            raise ValueError(f"Failed to get files for package {package_id}") 