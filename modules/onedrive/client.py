"""
OneDrive client for Microsoft Graph API integration
"""
import logging
from typing import Optional, Dict, Any
import requests
from config import config
from modules.utils.logger import log_error_with_traceback, StructuredLogger


class OneDriveClient:
    """OneDrive client for file operations via Microsoft Graph API"""
    
    def __init__(self):
        """Initialize OneDrive client"""
        self.logger = StructuredLogger(__name__)
        
        # Validate Microsoft Graph configuration
        if not all([
            config.MICROSOFT_CLIENT_ID,
            config.MICROSOFT_CLIENT_SECRET,
            config.MICROSOFT_TENANT_ID
        ]):
            self.logger.warning("Microsoft Graph configuration is incomplete")
        
        self.access_token: Optional[str] = None
        self.base_url = "https://graph.microsoft.com/v1.0"
        
        self.logger.info("OneDrive client initialized")
    
    def authenticate(self) -> bool:
        """
        Authenticate with Microsoft Graph API
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # TODO: Implement proper OAuth2 flow for production
            # For now, this is a placeholder for client credentials flow
            
            auth_url = f"https://login.microsoftonline.com/{config.MICROSOFT_TENANT_ID}/oauth2/v2.0/token"
            
            data = {
                'client_id': config.MICROSOFT_CLIENT_ID,
                'client_secret': config.MICROSOFT_CLIENT_SECRET,
                'scope': 'https://graph.microsoft.com/.default',
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(auth_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                self.logger.info("Successfully authenticated with Microsoft Graph")
                return True
            else:
                self.logger.error("Authentication failed", 
                                status_code=response.status_code,
                                response=response.text)
                return False
                
        except Exception as e:
            log_error_with_traceback(
                logging.getLogger(__name__), 
                "Authentication error", 
                e
            )
            return False
    
    def upload_file(self, file_content: bytes, file_name: str, folder_path: str = None) -> Optional[Dict[str, Any]]:
        """
        Upload file to OneDrive
        
        Args:
            file_content: File content as bytes
            file_name: Name of the file
            folder_path: Optional folder path (defaults to root folder)
            
        Returns:
            Upload response or None if failed
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return None
            
            # Determine upload path
            if folder_path:
                upload_path = f"/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}/{folder_path}/{file_name}:/content"
            else:
                upload_path = f"/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}/{file_name}:/content"
            
            url = f"{self.base_url}{upload_path}"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/octet-stream'
            }
            
            response = requests.put(url, headers=headers, data=file_content)
            
            if response.status_code in [200, 201]:
                self.logger.info("File uploaded successfully", 
                               file_name=file_name,
                               folder_path=folder_path)
                return response.json()
            else:
                self.logger.error("File upload failed",
                                file_name=file_name,
                                status_code=response.status_code,
                                response=response.text)
                return None
                
        except Exception as e:
            log_error_with_traceback(
                logging.getLogger(__name__), 
                f"File upload error for {file_name}", 
                e
            )
            return None
    
    def create_folder(self, folder_name: str, parent_path: str = None) -> Optional[Dict[str, Any]]:
        """
        Create folder in OneDrive
        
        Args:
            folder_name: Name of the folder to create
            parent_path: Parent folder path (defaults to root)
            
        Returns:
            Folder creation response or None if failed
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return None
            
            # Determine parent path
            if parent_path:
                url = f"{self.base_url}/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}/{parent_path}:/children"
            else:
                url = f"{self.base_url}/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}:/children"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'name': folder_name,
                'folder': {},
                '@microsoft.graph.conflictBehavior': 'rename'
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                self.logger.info("Folder created successfully", 
                               folder_name=folder_name,
                               parent_path=parent_path)
                return response.json()
            else:
                self.logger.error("Folder creation failed",
                                folder_name=folder_name,
                                status_code=response.status_code,
                                response=response.text)
                return None
                
        except Exception as e:
            log_error_with_traceback(
                logging.getLogger(__name__), 
                f"Folder creation error for {folder_name}", 
                e
            )
            return None
    
    def list_files(self, folder_path: str = None) -> Optional[list]:
        """
        List files in OneDrive folder
        
        Args:
            folder_path: Folder path (defaults to root)
            
        Returns:
            List of files or None if failed
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return None
            
            # Determine folder path
            if folder_path:
                url = f"{self.base_url}/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}/{folder_path}:/children"
            else:
                url = f"{self.base_url}/me/drive/root:/{config.ONEDRIVE_ROOT_FOLDER}:/children"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('value', [])
            else:
                self.logger.error("File listing failed",
                                folder_path=folder_path,
                                status_code=response.status_code,
                                response=response.text)
                return None
                
        except Exception as e:
            log_error_with_traceback(
                logging.getLogger(__name__), 
                f"File listing error for {folder_path}", 
                e
            )
            return None
    
    def cleanup(self):
        """Cleanup resources"""
        self.access_token = None
        self.logger.info("OneDrive client cleaned up")