import subprocess
import sys
import os

def create_venv():
    """Create Python 3.12 virtual environment"""
    print("Creating Python 3.12 virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv", "--python=python3.12"])

def install_requirements():
    """Install requirements in virtual environment"""
    print("Installing requirements...")
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])

def setup_env():
    """Setup environment file"""
    if not os.path.exists(".env"):
        print("Creating .env file from template...")
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())
        print("Please update .env file with your OpenAI API key")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    setup_env()
    print("\nSetup complete!")
    print("1. Update .env file with your OpenAI API key")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run: python -m app.main")