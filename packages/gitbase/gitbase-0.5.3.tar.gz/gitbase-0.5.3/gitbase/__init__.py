"""
GitBase: A module for managing data storage in a GitHub repository, allowing reading, writing, uploading, and deleting files.

Classes:
- GitBase: Handles interactions with a GitHub repository for file storage and retrieval.
    - param token (str): The GitHub access token for authentication.
    - param repo_owner (str): The owner of the GitHub repository.
    - param repo_name (str): The name of the GitHub repository.
    - param branch (str, default='main'): The branch where files are stored.

    Methods:
    - read_data(path: str) -> Tuple[Optional[str], Optional[str]]:
        Reads a file from the repository and returns its content and SHA.
        - param path (str): The file path in the repository.
        - returns: A tuple containing the file content and SHA identifier.

    - write_data(path: str, data: str, message: str = "Updated data") -> int:
        Writes or updates a file in the repository.
        - param path (str): The file path in the repository.
        - param data (str): The data to be written.
        - param message (str): The commit message for the update.
        - returns: HTTP status code of the operation.

    - delete_data(path: str, message: str = "Deleted data") -> int:
        Deletes a file from the repository.
        - param path (str): The file path in the repository.
        - param message (str): The commit message for the deletion.
        - returns: HTTP status code of the operation.

    - upload_file(file_path: str, remote_path: str, message: str = "Uploaded file") -> int:
        Uploads a local file to the repository.
        - param file_path (str): The local file path.
        - param remote_path (str): The target file path in the repository.
        - param message (str): The commit message for the upload.
        - returns: HTTP status code of the operation.

    - download_file(remote_path: str, local_path: str) -> int:
        Downloads a file from the repository to the local system.
        - param remote_path (str): The file path in the repository.
        - param local_path (str): The destination path on the local system.
        - returns: HTTP status code of the operation.

    - get_file_last_modified(path: str) -> Optional[float]:
        Retrieves the last modified timestamp of a file in the repository.
        - param path (str): The file path in the repository.
        - returns: The timestamp of the last modification or None if unavailable.

Functions:
- data_loaded() -> bool:
    Checks whether data has been successfully loaded.
    - returns: True if data has been loaded, False otherwise.

- init(show_credits: bool = True) -> None:
    Initializes the GitBase module, displaying credits if enabled.
    - param show_credits (bool): Whether to display credits.
    
---

The 'DataSystem' extension of the 'GitBase' module: Allows for general data management excluding account/player data management.

Consists of: 
* KeyValue (class): Represents a key-value pair for storing data.
    - param: key (str): The key to represent the pair.
    - param: value (Any): The value connected to the key. Can be anything.

* DataSystem (class): Handles data storage and retrieval, supporting online GitBase and offline backups.
    - param: db (GitBase): The database object for interacting with GitBase.
    - param: encryption_key (bytes): Key for encrypting and decrypting data.
    - param: fernet (Fernet): Encryption handler from the `cryptography` package.
    
    Methods:
        - encrypt_data(data: str) -> bytes: Encrypts a string using the configured encryption key.
            - param: data (str): The plaintext string to encrypt.
            - returns: bytes: The encrypted data as bytes.

        - decrypt_data(encrypted_data: bytes) -> str: Decrypts a string using the configured encryption key.
            - param: encrypted_data (bytes): The encrypted data to decrypt.
            - returns: str: The decrypted plaintext string.

        - save_data(key: str, value: Any, path: str = "data", encryption: bool = False) -> None: 
            Saves data to GitBase or an offline backup.
            - param: key (str): The key to associate with the data.
            - param: value (Any): The value to save.
            - param: path (str): The directory path to save the data in.
            - param: encryption (bool): Whether to encrypt the data before saving.

        - load_data(key: str, encryption: bool, path: str = "data") -> Optional[Any]: 
            Loads data from GitBase or an offline backup.
            - param: key (str): The key of the data to load.
            - param: encryption (bool): Whether to decrypt the data after loading.
            - param: path (str): The directory path to load the data from.
            - returns: Optional[Any]: The loaded data, or None if not found.

        - save_offline_data(key: str, value: Any) -> None: 
            Saves data to an offline backup file.
            - param: key (str): The key to associate with the data.
            - param: value (Any): The value to save.

        - load_offline_data(key: str) -> Optional[Any]: 
            Loads data from an offline backup file.
            - param: key (str): The key of the data to load.
            - returns: Optional[Any]: The loaded data, or None if not found.

        - delete_data(key: str, path: str = "data", delete_offline: bool = False) -> None: 
            Deletes data from GitBase and optionally from offline storage.
            - param: key (str): The key of the data to delete.
            - param: path (str): The path to the data.
            - param: delete_offline (bool): Whether to delete the offline backup as well.

        - get_all(path: str = "data") -> Dict[str, Any]: 
            Retrieves all key-value pairs stored in the system.
            - param: path (str): The directory path to retrieve data from.
            - returns: Dict[str, Any]: A dictionary of all key-value pairs.

        - chunk(file_path: str, output_dir: str, duration_per_chunk: int = 90) -> None: 
            Splits a video file into smaller chunks.
            - param: file_path (str): Path to the input video file.
            - param: output_dir (str): Directory to save the video chunks.
            - param: duration_per_chunk (int): Duration per chunk in seconds.
            - Notes: Ensures a minimum of 4 chunks.

        - pack(chunks_dir: str, output_file: str) -> None: 
            Combines video chunks into a single file.
            - param: chunks_dir (str): Directory containing the video chunks.
            - param: output_file (str): Path for the combined output file.
            - Notes: Assumes chunks are in order and in the same format.

        - partial_pack(chunks_dir: str, output_file: str, start_chunk: int, end_chunk: int) -> None: 
            Combines a range of video chunks into a single file.
            - param: chunks_dir (str): Directory containing the video chunks.
            - param: output_file (str): Path for the combined output file.
            - param: start_chunk (int): Starting chunk number.
            - param: end_chunk (int): Ending chunk number.
            - Notes: Assumes chunks are in order and in the same format.
            
---

The 'PlayerDataSystem' extension of the 'GitBase' module: Manages player account data with support for online storage via GitBase and offline backups.

Consists of: 
* PlayerDataSystem (class): Handles player data storage, retrieval, and encryption, supporting GitBase for online persistence and local backups.
    - param: db (GitBase): The database object for interacting with GitBase.
    - param: encryption_key (bytes): Key for encrypting and decrypting player data.
    - param: fernet (Fernet): Encryption handler from the `cryptography` package.

    Methods:
        - encrypt_data(data: str) -> bytes: Encrypts a string using the configured encryption key.
            - param: data (str): The plaintext string to encrypt.
            - returns: bytes: The encrypted data as bytes.

        - decrypt_data(encrypted_data: bytes) -> str: Decrypts a string using the configured encryption key.
            - param: encrypted_data (bytes): The encrypted data to decrypt.
            - returns: str: The decrypted plaintext string.

        - save_account(username: str, player_instance: Any, encryption: bool, attributes: Optional[List[str]] = None, path: str = "players") -> None: 
            Saves a player's account data to GitBase or an offline backup.
            - param: username (str): The player's username.
            - param: player_instance (Any): The player instance containing data to save.
            - param: encryption (bool): Whether to encrypt the data before saving.
            - param: attributes (Optional[List[str]]): Specific attributes to save; defaults to all.
            - param: path (str): The directory path to save the data in.

        - save_offline_account(username: str, player_instance: Any, attributes: Optional[List[str]] = None) -> None: 
            Saves player data to an offline backup file.
            - param: username (str): The player's username.
            - param: player_instance (Any): The player instance containing data to save.
            - param: attributes (Optional[List[str]]): List of attributes to save; defaults to all.

        - load_account(username: str, player_instance: Any, encryption: bool) -> None: 
            Loads a player's account data from GitBase or an offline backup.
            - param: username (str): The player's username.
            - param: player_instance (Any): The player instance to populate with data.
            - param: encryption (bool): Whether to decrypt the data after loading.

        - load_offline_account(username: str, player_instance: Any) -> None: 
            Loads player data from an offline backup file.
            - param: username (str): The player's username.
            - param: player_instance (Any): The player instance to populate with data.

        - delete_account(username: str, delete_offline: bool = False) -> None: 
            Deletes a player's account data from GitBase and optionally from offline storage.
            - param: username (str): The player's username.
            - param: delete_offline (bool): Whether to delete the offline backup as well.

        - get_all(path: str = "players") -> Dict[str, Any]: 
            Retrieves all stored player accounts.
            - param: path (str): The directory path to retrieve data from.
            - returns: Dict[str, Any]: A dictionary of all player accounts.
"""

from .gitbase import GitBase, data_loaded, init
from .playerDataSystem import PlayerDataSystem
from .dataSystem import DataSystem, KeyValue
from .multibase import MultiBase
from fancyutil import NotificationManager as nm
NotificationManager: nm = nm()

__all__ = ["GitBase", "data_loaded", "PlayerDataSystem", "DataSystem", "KeyValue", "MultiBase", "NotificationManager", "init"]