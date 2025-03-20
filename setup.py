import os
import platform

print("Setting up the project...")

# Checks if the virtual environment exists.
#VENV_DIR = "venv"
#if not os.path.exists(VENV_DIR):
#    print("No virtual environment detected. Creating one...")
#    os.system(f"python -m venv {VENV_DIR}")
#
# Activates the virtual environment
#if platform.system() == "Windows":
#    ACTIVATE_CMD = f"{VENV_DIR}\\Scripts\\activate"
#else:
#    ACTIVATE_CMD = f"source {VENV_DIR}/bin/activate"

#print(f"Activating virtual environment: {ACTIVATE_CMD}")
#os.system(ACTIVATE_CMD)

# Installs dependencies
print("Installing dependencies...")
os.system("pip install -r app/requirements.txt")

# Runs Docker
run_docker = input("Do you want to run 'docker-compose up --build -d'? (y/n): ").strip().lower()
if run_docker == "y":
    print("Running Docker Compose...")
    os.system("docker-compose up --build -d")
else:
    print("Skipping Docker setup.")

# Resets the database
DB_PATH = "app/db.sqlite3"
if os.path.exists(DB_PATH):
    reset_db = input(
        "Do you want to delete the local database (db.sqlite3)? (y/n): ").strip().lower()
    if reset_db == "y":
        print("Deleting database...")
        os.remove(DB_PATH)

        print("Recreating migrations...")
        os.system("python app/manage.py makemigrations")

        print("Running migrations...")
        os.system("python app/manage.py migrate")

# Creates a superuser
create_superuser = input("👤 Do you want to create a superuser? (y/n): ").strip().lower()
if create_superuser == "y":
    os.system("python app/manage.py createsuperuser")

# Starts the Django server
print("Starting Django server in a new terminal...")
os.system("python app/manage.py runserver")

print("Setup complete!")
