#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Installation Validator
Quick script to verify installation for new users
"""

import sys
import importlib

def validate_installation():
    """Validate installation for new users"""
    print("🫀 ECG AI Heart Diagnosis - Installation Validator")
    print("=" * 55)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version compatible")
    
    # Check required modules
    required_modules = {
        'customtkinter': '🎨 Modern GUI Framework',
        'matplotlib': '📊 Data Plotting',
        'numpy': '🔢 Numerical Computing', 
        'serial': '🔌 Serial Communication',
        'requests': '🌐 HTTP Requests',
        'psutil': '📈 Performance Monitoring',
        'PIL': '🖼️  Image Processing'
    }
    
    print(f"\\n📦 Checking {len(required_modules)} Required Modules:")
    
    success_count = 0
    for module, description in required_modules.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {module:15} - {description}")
            success_count += 1
        except ImportError:
            print(f"   ❌ {module:15} - {description} (MISSING)")
    
    # Optional modules
    optional_modules = {
        'PyQt5': '📱 Legacy GUI (optional)',
        'pyqtgraph': '📊 Legacy Plotting (optional)'
    }
    
    print(f"\\n📋 Checking {len(optional_modules)} Optional Modules:")
    for module, description in optional_modules.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {module:15} - {description}")
        except ImportError:
            print(f"   ⚠️  {module:15} - {description} (optional)")
    
    # Overall result
    print(f"\\n📊 Installation Status: {success_count}/{len(required_modules)} required modules")
    
    if success_count == len(required_modules):
        print("\\n🎉 Installation Validation: SUCCESS!")
        print("✅ All required modules are installed and working")
        print("🚀 Ready to launch ECG AI Heart Diagnosis")
        
        # Show launch commands
        print("\\n🚀 Launch Commands:")
        print("   Modern GUI:  python launch_modern_gui.py")
        print("   Legacy GUI:  python -m ecg_receiver.main")
        
        return True
    else:
        print("\\n❌ Installation Validation: FAILED")
        missing_count = len(required_modules) - success_count
        print(f"⚠️  {missing_count} required modules missing")
        print("\\n🔧 To fix installation:")
        print("   pip install -r requirements.txt")
        print("   python validate_installation.py")
        
        return False

if __name__ == "__main__":
    success = validate_installation()
    if len(sys.argv) > 1 and sys.argv[1] == "--no-wait":
        # Non-interactive mode for automated testing
        pass
    else:
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            # Handle case where input is not available (e.g., in scripts)
            pass
    sys.exit(0 if success else 1)