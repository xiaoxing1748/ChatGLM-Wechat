import os
import shutil
import subprocess
import sys
import platform


def create_venv():
    print("Creating virtual environment...")
    if platform.system() == "Windows":
        subprocess.run(["python", "-m", "venv", ".venv"], check=True)
    else:
        subprocess.run(["python3", "-m", "venv", ".venv"], check=True)


def initialize_config():
    config_file = "config.yaml"
    backup_file = "config.yaml.backup"

    if not os.path.exists(config_file):
        if os.path.exists(backup_file):
            shutil.copy(backup_file, config_file)
        else:
            print(f"Error: {backup_file} not found.")
            sys.exit(1)

        print(
            f"Config file {config_file} created. Please edit it and press any key to exit.")
        input()
        sys.exit(0)


def start_venv():
    venv_python = os.path.join(
        "venv", "bin" if platform.system() != "Windows" else "Scripts", "python")
    config_file = "config.yaml"

    if os.path.exists(config_file):
        print("Starting server...")
        subprocess.run([venv_python, "test.py"], check=True)
    else:
        print("Error: config.yaml not found. Please run the script again after editing config.yaml.")
        sys.exit(1)


def start():
    config_file = "config.yaml"
    if os.path.exists(config_file):
        print("Starting server...")
        subprocess.run(["python", "test.py"], check=True)
    else:
        print("Error: config.yaml not found. Please run the script again after editing config.yaml.")
        sys.exit(1)


if __name__ == "__main__":
    venv_path = "venv"

    if not os.path.exists(venv_path):
        create_venv()

    # Change to the script's directory
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # initialize_config()

    # start()

    # start_venv()
