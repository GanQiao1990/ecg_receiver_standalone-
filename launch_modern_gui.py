#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Modern Tkinter GUI Launcher
Entry point for the modern redesigned GUI using CustomTkinter
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check and install required dependencies for modern GUI"""
    required_packages = [
        'customtkinter',
        'matplotlib', 
        'Pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0]
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("🔧 Installing missing dependencies for modern GUI...")
        print(f"Missing: {', '.join(missing_packages)}")
        
        # Multiple PyPI mirrors for better connectivity
        mirrors = [
            "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple",
            "https://pypi.douban.com/simple/",
            "https://mirrors.aliyun.com/pypi/simple/",
            "https://pypi.mirrors.ustc.edu.cn/simple/"
        ]
        
        success = False
        for mirror in mirrors:
            print(f"🔄 Trying mirror: {mirror.split('//')[1].split('/')[0]}")
            try:
                for package in missing_packages:
                    cmd = [sys.executable, "-m", "pip", "install", package, "-i", mirror, "--timeout", "30"]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
                print("✅ Dependencies installed successfully!")
                success = True
                break
                
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"❌ Failed with {mirror.split('//')[1].split('/')[0]}: Network error")
                continue
        
        if not success:
            print("\n❌ All mirrors failed. Network connectivity issues detected.")
            print("\n📋 Manual installation options:")
            print("Option 1 - Use mamba (recommended):")
            print("  mamba install pillow matplotlib")
            print("  pip install customtkinter --no-deps")
            print("\nOption 2 - Try offline mode:")
            for package in missing_packages:
                print(f"  pip install {package} --user --timeout 60")
            print("\nOption 3 - Use basic GUI (fallback):")
            print("  python launch_basic_gui.py")
            
            return False
    
    return True

def main():
    """Launch the modern ECG GUI"""
    print("🫀 ECG AI Heart Diagnosis - Modern GUI")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies before running.")
        sys.exit(1)
    
    # Import and run the modern GUI
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from ecg_receiver.gui_tkinter.main_window_modern import ModernECGMainWindow
        
        print("🚀 Starting modern ECG AI diagnosis interface...")
        app = ModernECGMainWindow()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all required packages are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
