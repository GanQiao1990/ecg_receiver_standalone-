#!/usr/bin/env python3
"""
ECM_LLM Windows Installation Helper
This script helps install the ECG Monitor with AI diagnosis on Windows systems.
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 70)
    print("🫀 ECG Monitor with AI Diagnosis - Windows Installer")
    print("=" * 70)
    print("This script will help install ECM_LLM on your Windows system.\n")

def check_python():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required!")
        print("Please upgrade Python: https://www.python.org/downloads/")
        return False
    
    print("✅ Python version is compatible")
    return True

def upgrade_pip():
    """Upgrade pip to latest version."""
    print("\n📦 Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        print("✅ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: pip upgrade failed: {e}")
        return False

def install_requirements():
    """Install required packages."""
    print("\n📚 Installing required packages...")
    
    # List of packages to install individually (more reliable on Windows)
    packages = [
        "pyserial>=3.5",
        "numpy>=1.24.0", 
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ]
    
    # Install PyQt5 separately (often problematic)
    print("Installing PyQt5...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5==5.15.7"], 
                      check=True, capture_output=True, text=True)
        print("✅ PyQt5 installed successfully")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "pyqtgraph>=0.13.0"], 
                      check=True, capture_output=True, text=True)
        print("✅ pyqtgraph installed successfully")
        
    except subprocess.CalledProcessError as e:
        print("❌ PyQt5 installation failed. Trying alternative...")
        try:
            # Try with --only-binary for pre-compiled wheels
            subprocess.run([sys.executable, "-m", "pip", "install", "--only-binary=all", "PyQt5"], 
                          check=True, capture_output=True, text=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "pyqtgraph"], 
                          check=True, capture_output=True, text=True)
            print("✅ PyQt5 installed with binary wheels")
        except subprocess.CalledProcessError as e2:
            print(f"❌ PyQt5 installation failed: {e2}")
            print("Please install PyQt5 manually:")
            print("1. Download from: https://www.riverbankcomputing.com/software/pyqt/download5")
            print("2. Or try: conda install pyqt (if using Anaconda)")
            return False
    
    # Install other packages
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True, text=True)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def setup_environment():
    """Setup environment configuration."""
    print("\n⚙️ Setting up environment...")
    
    env_example = ".env.example"
    env_file = ".env"
    
    if os.path.exists(env_example) and not os.path.exists(env_file):
        try:
            import shutil
            shutil.copy(env_example, env_file)
            print(f"✅ Created {env_file} from template")
            print(f"📝 Please edit {env_file} and add your Gemini API key")
        except Exception as e:
            print(f"⚠️ Could not create {env_file}: {e}")
            print(f"Please manually copy {env_example} to {env_file}")
    
    return True

def test_installation():
    """Test the installation."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        print("Testing imports...")
        import serial
        print("✅ pyserial")
        
        import numpy
        print("✅ numpy") 
        
        import requests
        print("✅ requests")
        
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5")
        
        import pyqtgraph
        print("✅ pyqtgraph")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv")
        
        # Test main modules
        import ecg_diagnosis
        print("✅ ecg_diagnosis module")
        
        from ecg_receiver.main import main
        print("✅ ecg_receiver module")
        
        print("\n🎉 Installation test successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_next_steps():
    """Show next steps to user."""
    print("\n" + "=" * 70)
    print("🎯 INSTALLATION COMPLETE!")
    print("=" * 70)
    print("Next steps:")
    print("1. 🔑 Get Gemini API key from: https://api.gptnb.ai/")
    print("2. 📝 Edit .env file and add your API key")
    print("3. 🔌 Connect your ESP32 ECG device")
    print("4. 🚀 Launch application: python -m ecg_receiver.main")
    print("\nTesting commands:")
    print("• Test diagnosis: python test_diagnosis.py")
    print("• System check: python demo.py")
    print("\n📚 Documentation:")
    print("• Main guide: README.md")
    print("• Windows help: WINDOWS_INSTALL.md")
    print("• Deployment: DEPLOYMENT.md")
    print("=" * 70)

def main():
    """Main installation function."""
    print_header()
    
    # Check system
    if platform.system() != "Windows":
        print("⚠️ This installer is designed for Windows.")
        print("For other systems, please follow README.md instructions.")
        return
    
    # Check Python
    if not check_python():
        input("\nPress Enter to exit...")
        return
    
    # Upgrade pip
    upgrade_pip()
    
    # Install packages
    if not install_requirements():
        print("\n❌ Installation failed!")
        input("Press Enter to exit...")
        return
    
    # Setup environment
    setup_environment()
    
    # Test installation
    if test_installation():
        show_next_steps()
    else:
        print("\n⚠️ Installation completed but tests failed.")
        print("Please check WINDOWS_INSTALL.md for troubleshooting.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()