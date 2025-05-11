"""
Setup script for the SubZero agent.

This script:
1. Creates a virtual environment
2. Activates the virtual environment
3. Installs the required dependencies
4. Creates a .env file for API keys
"""

import os
import sys
import subprocess
import platform
import shutil

def create_virtual_environment():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created successfully.")

def activate_virtual_environment():
    """Activate the virtual environment and return the activation command."""
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        activate_cmd = f"{activate_script}"
        print(f"To activate the virtual environment, run: {activate_cmd}")
        return activate_cmd
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        activate_cmd = f"source {activate_script}"
        print(f"To activate the virtual environment, run: {activate_cmd}")
        return activate_cmd

def install_dependencies(activate_cmd):
    """Install the required dependencies."""
    print("Installing dependencies...")
    
    if platform.system() == "Windows":
        pip_cmd = os.path.join("venv", "Scripts", "pip")
    else:
        pip_cmd = os.path.join("venv", "bin", "pip")
    
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully.")

def create_env_file():
    """Create a .env file for API keys."""
    if not os.path.exists(".env"):
        print("Creating .env file...")
        shutil.copy(".env.example", ".env")
        print(".env file created successfully.")
        print("Please edit the .env file and add your API keys.")
    else:
        print(".env file already exists.")

def main():
    """Main function."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the current directory
    os.chdir(current_dir)
    
    # Create a virtual environment
    create_virtual_environment()
    
    # Activate the virtual environment
    activate_cmd = activate_virtual_environment()
    
    # Install dependencies
    install_dependencies(activate_cmd)
    
    # Create .env file
    create_env_file()
    
    print("\nSetup completed successfully!")
    print("\nTo run the simple demo:")
    if platform.system() == "Windows":
        print("1. venv\\Scripts\\activate")
    else:
        print("1. source venv/bin/activate")
    print("2. python simple_demo.py")
    
    print("\nTo run the full demo (requires API keys):")
    if platform.system() == "Windows":
        print("1. venv\\Scripts\\activate")
    else:
        print("1. source venv/bin/activate")
    print("2. python demo.py")

if __name__ == "__main__":
    main()
