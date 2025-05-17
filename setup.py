import platform
import subprocess
import sys
from pathlib import Path

print("Setting up the project...")

VENV_DIR = Path(".venv")
VENV_BIN = "Scripts" if platform.system() == "Windows" else "bin"
VENV_PYTHON = VENV_DIR / VENV_BIN / ("python.exe" if platform.system() == "Windows" else "python")

REQ_FILE = Path("app/requirements.txt")
DB_PATH = Path("app/db.sqlite3")
FIXTURES = [
    "app/fixtures/initial_learning_content.json",
    "app/fixtures/initial_items_content.json",
    "app/fixtures/initial_superusers_content.json",
    "app/fixtures/initial_friendships_content.json",
    "app/fixtures/initial_groups_content.json"
    "app/fixtures/initial_achievements_content.json"
]

def run_cmd(cmd, description=""):
    if description:
        print(f"{description}...")
    subprocess.run([str(c) for c in cmd], check=True)


def load_fixtures():
    for fixture in FIXTURES:
        run_cmd([VENV_PYTHON, "app/manage.py", "loaddata", fixture], f"Loading fixture {fixture}")


# Create virtual environment if it does not exist
if not (VENV_DIR / VENV_BIN).exists():
    run_cmd([sys.executable, "-m", "venv", VENV_DIR], "Creating virtual environment")

# Install Python dependencies inside the virtual environment
if REQ_FILE.exists():
    run_cmd([VENV_PYTHON, "-m", "pip", "install", "-r", REQ_FILE], "Installing dependencies")
else:
    print(f"Warning: {REQ_FILE} not found. Skipping dependency installation.")

# Handle database setup
if not DB_PATH.exists():
    run_cmd([VENV_PYTHON, "app/manage.py", "migrate"], "Applying migrations")
    load_fixtures()
else:
    if input("Do you want to delete and reset the local database? (y/n): ").strip().lower() == "y":
        if input("Are you sure? This action is irreversible! (y/n): ").strip().lower() == "y":
            try:
                DB_PATH.unlink()
            except PermissionError:
                print(
                    "Cannot delete the database file. It might be in use. Please close any running servers, consoles, or database tools.")
            else:
                run_cmd([VENV_PYTHON, "app/manage.py", "migrate"], "Re-applying migrations")
                load_fixtures()

# Run Docker Compose (currently commented out for future use)
# run_docker = input("Do you want to run 'docker-compose up --build -d'? (y/n): ").strip().lower()
# if run_docker == "y":
#     try:
#         # Check if Docker is available first
#         subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
#         run_cmd(["docker-compose", "up", "--build", "-d"], "Running Docker Compose")
#     except subprocess.CalledProcessError:
#         print("\n" + "=" * 80)
#         print("ERROR: Docker is not running or not installed.")
#         print("Please start Docker Desktop and try again.")
#         print("=" * 80 + "\n")
#         print("This is a critical error. The application might not work correctly without Docker running.")

# Create a superuser (Currently commented out because fixtures already create superusers by default)
# create_superuser = input("Do you want to create a superuser manually? (y/n): ").strip().lower()
# if create_superuser == "y":
#     run_cmd([VENV_PYTHON, "app/manage.py", "createsuperuser"], "Creating superuser")

# Info
print("\nSetup complete.")
print("5 superusers created with matching usernames and passwords:")
for i in range(1, 6):
    print(f"  Username: {i}   Password: {i}")

# Start the Django development server
if input("\nDo you want to run the Django server now? (y/n): ").strip().lower() == "y":
    run_cmd([VENV_PYTHON, "app/manage.py", "runserver"], "Starting Django server")
