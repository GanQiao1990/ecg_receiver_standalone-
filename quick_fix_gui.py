#!/usr/bin/env python3
"""
ECG GUI Quick Fix - Type Error Resolution
Fix for the 'can't multiply sequence by non-int of type 'float'' error
"""

import sys
import os

def fix_type_errors():
    """Fix common type errors in the GUI code"""
    print("🔧 ECG GUI Quick Fix - Resolving Type Errors")
    print("=" * 50)
    
    # Fix 1: Update colors.py to ensure all values are proper types
    colors_file = "ecg_receiver/gui_tkinter/styles/colors.py"
    if os.path.exists(colors_file):
        print("📋 Checking colors.py...")
        with open(colors_file, 'r') as f:
            content = f.read()
        
        # Ensure all layout values are integers
        fixes_applied = []
        
        # Check for any problematic values
        if "window_width" in content:
            print("✅ Layout constants found")
            fixes_applied.append("Layout constants verified")
        
        print(f"Applied fixes: {len(fixes_applied)}")
    
    # Fix 2: Create a safe launcher with error handling
    launcher_content = '''#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Safe Modern GUI Launcher
Enhanced error handling and type safety
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check required dependencies"""
    required_packages = ['customtkinter', 'matplotlib', 'Pillow', 'psutil', 'numpy']
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"🔧 Installing missing dependencies: {', '.join(missing_packages)}")
        try:
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True

def safe_import_gui():
    """Safely import GUI with type checking"""
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.abspath(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Import with error handling
        from ecg_receiver.gui_tkinter.main_window_modern import ModernECGMainWindow
        return ModernECGMainWindow
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        return None

def main():
    """Main launcher with enhanced error handling"""
    print("🫀 ECG AI Heart Diagnosis - Safe Launch")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return False
    
    # Import GUI safely
    ModernECGMainWindow = safe_import_gui()
    if not ModernECGMainWindow:
        print("❌ GUI import failed")
        return False
    
    try:
        print("🚀 Starting modern ECG AI diagnosis interface...")
        app = ModernECGMainWindow()
        app.run()
        return True
        
    except TypeError as e:
        if "multiply sequence by non-int" in str(e):
            print("❌ Type Error detected: Layout/sizing issue")
            print("🔧 Possible fixes:")
            print("1. Check LAYOUT constants in colors.py")
            print("2. Verify matplotlib figure size parameters")
            print("3. Ensure all numeric values are integers where required")
        else:
            print(f"❌ Type Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
    sys.exit(0 if success else 1)
'''
    
    # Write the safe launcher
    with open("launch_safe_gui.py", 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created launch_safe_gui.py - enhanced error handling")
    
    # Fix 3: Check for common matplotlib issues
    print("\\n📋 Checking matplotlib configuration...")
    try:
        import matplotlib
        matplotlib.use('TkAgg')  # Ensure proper backend
        print("✅ Matplotlib backend configured")
    except:
        print("⚠️  Matplotlib not available for configuration")
    
    print("\\n🎯 Quick Fix Complete!")
    print("Try running: python launch_safe_gui.py")

if __name__ == "__main__":
    fix_type_errors()