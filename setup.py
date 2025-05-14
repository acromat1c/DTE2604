import os
import platform
import subprocess
import sys

print("Setting up the project...")

VENV_DIR = ".venv"

# Creates virtual environment
venv_bin = "Scripts" if platform.system() == "Windows" else "bin"
if not os.path.exists(os.path.join(VENV_DIR, venv_bin)):
    print("No virtual environment detected. Creating one...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)

# Gets Python.exe from venv
venv_python = os.path.join(VENV_DIR, venv_bin, "python.exe" if platform.system() == "Windows" else "python")

# Installs dependencies in venv
REQ_FILE = "app/requirements.txt"
if os.path.exists(REQ_FILE):
    print("Installing dependencies from requirements.txt inside the virtual environment...")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", REQ_FILE], check=True)
else:
    print(f"Warning: {REQ_FILE} not found. Skipping dependency installation.")

print("Setup complete.")

# Runs Docker
run_docker = input("Do you want to run 'docker-compose up --build -d'? (y/n): ").strip().lower()
if run_docker == "y":
    if subprocess.run(["docker-compose", "--version"], capture_output=True).returncode == 0:
        print("Running Docker Compose...")
        subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    else:
        print("Warning: Docker is not installed or not running. Skipping Docker setup.")

# Database handling
DB_PATH = "app/db.sqlite3"
if not os.path.exists(DB_PATH):
    print("Database file not found. Creating db.sqlite3...")
    subprocess.run([venv_python, "app/manage.py", "migrate"], check=True)
    # loaddata
    subprocess.run([venv_python, "app/manage.py", "loaddata", "app/fixtures/initial_learning_content.json"], check=True)
else:
    reset_db = input("Do you want to delete the local database (db.sqlite3)? (y/n): ").strip().lower()
    if reset_db == "y":
        confirm_reset = input("Are you sure? This action is irreversible! (y/n): ").strip().lower()
        if confirm_reset == "y":
            print("Deleting database...")
            os.remove(DB_PATH)

#            print("Recreating migrations...")
#            subprocess.run([venv_python, "app/manage.py", "makemigrations"], check=True)

            print("Running migrations...")
            subprocess.run([venv_python, "app/manage.py", "migrate"], check=True)
            # loaddata
            subprocess.run([venv_python, "app/manage.py", "loaddata", "app/fixtures/initial_learning_content.json"], check=True)

# Creates a superuser
create_superuser = input("Do you want to create a superuser? (y/n): ").strip().lower()
if create_superuser == "y":
    subprocess.run([venv_python, "app/manage.py", "createsuperuser"], check=True)

# Start the Django

run_server = input("Do you want to run Django server? (y/n): ").strip().lower()
if run_server == "y":
    print("Starting Django server in the current terminal...")
    subprocess.run([venv_python, "app/manage.py", "runserver"], check=True)

print("Setup complete!")
