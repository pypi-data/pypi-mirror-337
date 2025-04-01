"""
MultiBase: A module for managing multiple GitBase instances, providing a seamless interface
to interact with several GitHub repositories for file storage and retrieval.

Classes:
- MultiBase:
    Handles interactions across multiple GitHub repositories by wrapping several GitBase
    instances. This allows operations to automatically switch repositories if one becomes full
    or unavailable.

    Parameters:
    - gitbases (List[Dict[str, str]]): A list of GitBase configuration dictionaries. Each
      dictionary should contain the keys 'token', 'repo_owner', 'repo_name', and optionally 'branch'
      (defaults to 'main').

    Methods:
    - write_data(path: str, data: str, message: str = "Updated data") -> int:
        Writes or updates a file in the first available GitBase. If the active GitBase fails to
        store the data (i.e., does not return status 200 or 201), the method will switch to the
        next GitBase in the list until the operation succeeds or all instances are exhausted.
    
    - read_data(path: str) -> Tuple[Optional[str], Optional[str]]:
        Reads a file from the first GitBase where the file is found, returning a tuple of the
        file's content and its SHA.
    
    - delete_data(path: str, message: str = "Deleted data") -> int:
        Deletes a file from all GitBase instances. Returns 200 if the deletion is successful
        in any repository, otherwise returns 404.
    
    - upload_file(file_path: str, remote_path: str, message: str = "Uploaded file") -> int:
        Uploads a local file to the first available GitBase. If the operation fails on the active
        GitBase, it will attempt the next one in sequence.
    
    - download_file(remote_path: str, local_path: str) -> int:
        Downloads a file from the first GitBase where the file exists and writes it to the
        local system. Returns 200 on success, or 404 if the file is not found in any repository.
    
    - get_file_last_modified(path: str) -> Optional[float]:
        Retrieves the most recent modification timestamp for a file by checking across all
        GitBase instances. Returns the latest timestamp found or None if the file is not available.
"""

import requests
import base64
from typing import Optional, Tuple, List, Dict, Union
from datetime import datetime
from .gitbase import GitBase

class MultiBase:
    def __init__(self, gitbases: List[Dict[str, str]]) -> None:
        """
        MultiBase allows using multiple GitBase instances in sequence when one gets full.
        :param gitbases: A list of GitBase configurations with 'token', 'repo_owner', 'repo_name', and 'branch'.
        """
        self.gitbases = [GitBase(**gb) for gb in gitbases]
        self.current_index = 0
    
    def _get_active_gitbase(self) -> Optional['GitBase']:
        """Returns the currently active GitBase instance."""
        if self.current_index < len(self.gitbases):
            return self.gitbases[self.current_index]
        return None
    
    def _switch_to_next_gitbase(self) -> bool:
        """Switches to the next GitBase if available."""
        if self.current_index + 1 < len(self.gitbases):
            self.current_index += 1
            return True
        return False
    
    def write_data(self, path: str, data: str, message: str = "Updated data") -> int:
        """Writes data to the first available GitBase, switching if needed."""
        while self.current_index < len(self.gitbases):
            gitbase = self._get_active_gitbase()
            if gitbase:
                status = gitbase.write_data(path, data, message)
                if status == 201 or status == 200:  # Successfully written
                    return status
                else:
                    if not self._switch_to_next_gitbase():
                        return status  # No more GitBases available
        return 507  # Insufficient Storage on all GitBases
    
    def read_data(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        """Reads data from the first GitBase where the file exists."""
        for gitbase in self.gitbases:
            content, sha = gitbase.read_data(path)
            if content is not None:
                return content, sha
        return None, None
    
    def delete_data(self, path: str, message: str = "Deleted data") -> int:
        """Deletes data from all GitBase instances."""
        status_codes = [gb.delete_data(path, message) for gb in self.gitbases]
        return 200 if any(status == 200 for status in status_codes) else 404
    
    def upload_file(self, file_path: str, remote_path: str, message: str = "Uploaded file") -> int:
        """Uploads a file using the first available GitBase, switching if needed."""
        while self.current_index < len(self.gitbases):
            gitbase = self._get_active_gitbase()
            if gitbase:
                status = gitbase.upload_file(file_path, remote_path, message)
                if status == 201 or status == 200:
                    return status
                else:
                    if not self._switch_to_next_gitbase():
                        return status
        return 507
    
    def download_file(self, remote_path: str, local_path: str) -> int:
        """Downloads a file from the first GitBase where it exists."""
        for gitbase in self.gitbases:
            status = gitbase.download_file(remote_path, local_path)
            if status == 200:
                return status
        return 404
    
    def get_file_last_modified(self, path: str) -> Optional[float]:
        """Returns the latest modified timestamp across all GitBase instances."""
        timestamps = [gb.get_file_last_modified(path) for gb in self.gitbases]
        valid_timestamps = [ts for ts in timestamps if ts is not None]
        return max(valid_timestamps, default=None)
