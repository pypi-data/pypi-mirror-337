# GitBase

GitBase is a Python package for custom databases powered by GitHub ("Gitbases"/"GitBase"), with encryption using `cryptography`. It provides Python developers with a quick and easy-to-use database solution without requiring knowledge of a new programming language. Additionally, GitBase offers offline backups, allowing users to save, load, and delete their data even without an internet connection. The online database will automatically sync with the latest file, whether offline or online.

---

## Latest Update
- Added `MultiBase`, a new version of `GitBase` which allows for multiple GitBases; old `from gitbase import GitBase` import now known as 'Legacy'
- Documented the code a bit more

---

## Example Code

```python
# Example for GitBase 0.5.1

from gitbase import GitBase, MultiBase, PlayerDataSystem, DataSystem
from cryptography.fernet import Fernet
import sys

# Initialize GitHub database and encryption key
GITHUB_TOKEN = "YOUR_TOKEN"
REPO_OWNER = "YOUR_GITHUB_USERNAME"
REPO_NAME = "YOUR_REPO_NAME"
encryption_key = Fernet.generate_key()

# Setup a single GitBase with GitHub credentials (legacy usage; remove if using MultiBase)
database = GitBase(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)

# Setup MultiBase with one or more GitBase configurations.
# You can add multiple configurations to handle repository fallback.
multi_database = MultiBase([
    {
        "token": GITHUB_TOKEN,
        "repo_owner": REPO_OWNER,
        "repo_name": REPO_NAME,
        "branch": "main"
    },
    # Additional GitBase configurations can be added here.
    # {"token": "YOUR_SECOND_TOKEN", "repo_owner": "YOUR_GITHUB_USERNAME", "repo_name": "YOUR_SECOND_REPO", "branch": "main"}
])

# Instantiate systems with both legacy and new
player_data_system = PlayerDataSystem(db=multi_database, encryption_key=encryption_key)
data_system = DataSystem(db=database, encryption_key=encryption_key)

# File upload and download examples using the legacy GitBase instance:
database.upload_file(file_path="my_file.txt", remote_path="saved_files/my_file.txt")
database.download_file(remote_path="saved_files/my_file.txt", local_path="files/my_file.txt")


# File upload and download examples using the new MultiBase instance:
multi_database.upload_file(file_path="my_second_file.txt", remote_path="saved_files/my_second_file.txt")
multi_database.download_file(remote_path="saved_files/my_second_file.txt", local_path="files/my_second_file.txt")

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

# Delete a specific player account
player_data_system.delete_account(username="john_doe")
```

---

## Consider Using [GitBase Web](https://tairerullc.vercel.app/products/extensions/gitbase-web)

### GitBase Web
GitBase Web is an extension of the Python project developed by Taireru LLC called GitBase. This extension allows developers to view all their saved data via the web. 

**Note:** To use GitBase Web, you **must**:
1. Use a private GitHub repository.
2. Host the website using a service such as [Vercel](https://vercel.com).

---

## Links
- **GitBase:** [https://tairerullc.vercel.app/products/packages/gitbase](https://tairerullc.vercel.app/products/packages/gitbase)
- **Website:** [https://tairerullc.vercel.app/](https://tairerullc.vercel.app/)

---

## Contact
For any inquiries, please email us at **tairerullc@gmail.com**. We’ll get back to you as soon as possible.  
Thank you for using GitBase, and happy coding!