#!/usr/bin/env python3
"""
Setup script for eCourts Scraper
Automates the installation and setup process.
"""

import os
import sys
import subprocess
import platform

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible."""
    print_header("CHECKING PYTHON VERSION")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print("Please upgrade your Python installation")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print_header("INSTALLING DEPENDENCIES")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print_header("CREATING DIRECTORIES")
    
    directories = [
        "output",
        "downloads",
        "logs",
        "templates"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")

def test_installation():
    """Test the installation."""
    print_header("TESTING INSTALLATION")
    
    try:
        # Test imports
        print("Testing imports...")
        import requests
        import beautifulsoup4
        import click
        import flask
        print("✅ All required modules imported successfully")
        
        # Test main script
        print("Testing main script...")
        result = subprocess.run([sys.executable, "ecourts_scraper.py", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Main script is working")
        else:
            print("❌ Main script test failed")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_sample_config():
    """Create sample configuration file."""
    print_header("CREATING CONFIGURATION")
    
    config_content = """# eCourts Scraper Configuration
# Copy this file to config.py and modify as needed

# Base URL for eCourts services
BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

# Request timeout in seconds
TIMEOUT = 30

# Number of retries for failed requests
RETRY_COUNT = 3

# Delay between requests in seconds
REQUEST_DELAY = 1

# Output directory
OUTPUT_DIR = "output"

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# Web interface settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = True
"""
    
    with open("config_sample.py", "w") as f:
        f.write(config_content)
    
    print("✅ Sample configuration created: config_sample.py")

def show_usage_instructions():
    """Show usage instructions."""
    print_header("USAGE INSTRUCTIONS")
    
    print("🚀 Your eCourts Scraper is ready!")
    print("\nQuick Start:")
    print("1. Command Line Interface:")
    print("   python ecourts_scraper.py --help")
    print("   python ecourts_scraper.py --cnr YOUR_CNR")
    print("   python ecourts_scraper.py --causelist")
    
    print("\n2. Web Interface:")
    print("   python web_interface.py")
    print("   Open browser to: http://localhost:5000")
    
    print("\n3. Testing:")
    print("   python test_scraper.py")
    print("   python demo_script.py")
    
    print("\n4. Documentation:")
    print("   Read README.md for detailed instructions")
    
    print("\n📁 Project Structure:")
    print("   ecourts_scraper.py    - Main scraper script")
    print("   web_interface.py     - Web interface")
    print("   test_scraper.py       - Test suite")
    print("   demo_script.py        - Demonstration script")
    print("   requirements.txt      - Dependencies")
    print("   README.md            - Documentation")

def main():
    """Main setup function."""
    print("🔧 eCourts Scraper Setup")
    print("Automated installation and configuration")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Test installation
    if not test_installation():
        print("\n❌ Setup failed at testing")
        sys.exit(1)
    
    # Create sample config
    create_sample_config()
    
    # Show usage instructions
    show_usage_instructions()
    
    print_header("SETUP COMPLETE")
    print("✅ eCourts Scraper is ready to use!")
    print("\nNext steps:")
    print("1. Test the installation: python test_scraper.py")
    print("2. Try the CLI: python ecourts_scraper.py --help")
    print("3. Start web interface: python web_interface.py")
    print("4. Create your demonstration video")
    print("5. Submit your GitHub repository")

if __name__ == "__main__":
    main()
