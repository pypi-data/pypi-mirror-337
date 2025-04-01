# Example for GitBase 0.5.3

from gitbase import MultiBase, PlayerDataSystem, DataSystem, NotificationManager
from cryptography.fernet import Fernet
import sys

# Initialize GitHub database and encryption key
GITHUB_TOKEN = "YOUR_TOKEN"
REPO_OWNER = "YOUR_GITHUB_USERNAME"
REPO_NAME = "YOUR_REPO_NAME"
encryption_key = Fernet.generate_key()

# Setup MultiBase with one or more GitBase configurations.
# You can add multiple configurations to handle repository fallback.
database = MultiBase([
    {
        "token": GITHUB_TOKEN,
        "repo_owner": REPO_OWNER,
        "repo_name": REPO_NAME,
        "branch": "main"
    },
    # Additional GitBase configurations can be added here.
    # {"token": "YOUR_SECOND_TOKEN", "repo_owner": "YOUR_GITHUB_USERNAME", "repo_name": "YOUR_SECOND_REPO", "branch": "main"}
])
# In legacy use case do
# from gitbase import GitBase
# database = GitBase(token=GITHUB_TOKEN, repo_owner=REPO_OWNER, repo_name=REPO_NAME, branch='main')

# Instantiate systems
player_data_system = PlayerDataSystem(db=database, encryption_key=encryption_key)
data_system = DataSystem(db=database, encryption_key=encryption_key)

# File upload and download examples
database.upload_file(file_path="my_file.txt", remote_path="saved_files/my_file.txt")
database.download_file(remote_path="saved_files/my_file.txt", local_path="files/my_file.txt")

# Define the Player class to manage individual player instances
class Player:
    def __init__(self, username, score, password):
        self.username = username
        self.score = score
        self.password = password

# Create a sample player instance
player = Player(username="john_doe", score=100, password="123")

# Save specific attributes of the player instance with encryption using MultiBase
player_data_system.save_account(
    username="john_doe",
    player_instance=player,
    encryption=True,
    attributes=["username", "score", "password"],
    path="players"
)

# Load player data
player_data_system.load_account(username="john_doe", player_instance=player, encryption=True)

# Placeholder functions for game flow
def load_game():
    print("Game starting...")

def main_menu():
    sys.exit("Exiting game...")

# Check if an account exists and validate user password
if player_data_system.get_all(path="players"):
    if player.password == input("Enter your password: "):
        print("Login successful!")
        load_game()
    else:
        print("Incorrect password!")
        main_menu()

# Save key-value data with encryption using MultiBase
data_system.save_data(key="key_name", value=69, path="data", encryption=True)

# Load and display a specific key-value pair
loaded_key_value = data_system.load_data(key="key_name", path="data", encryption=True)
print(f"Key: {loaded_key_value.key}, Value: {loaded_key_value.value}")

# Retrieve and display all key-value pairs in the data path
print("All stored data:", data_system.get_all(path="data"))

# Delete specific key-value data
data_system.delete_data(key="key_name", path="data")

# Retrieve and display all player accounts
print("All player accounts:", player_data_system.get_all(path="players"))

# Delete a specific player account and use NotificationManager to silence output
NotificationManager.hide()
player_data_system.delete_account(username="john_doe")
NotificationManager.show()