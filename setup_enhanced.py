#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Enhanced Installation Script
Automatically installs all dependencies and sets up the environment
"""

import sys
import os
import subprocess
import platform
import importlib
from pathlib import Path

def print_header():
    """Print installation header"""
    print("🫀 ECG AI Heart Diagnosis - Installation Setup")
    print("=" * 60)
    print("Modern GUI with AI-powered heart condition analysis")
    print("Powered by Gemini 2.5 Flash AI Model")
    print("=" * 60)
    
def check_python_version():
    """Check if Python version is compatible"""
    print("\n🐍 Checking Python Version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("✅ Python 3.8 or higher required")
        print("Please upgrade Python: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_pip():
    """Check if pip is available"""
    print("\n📦 Checking Package Manager...")
    
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip not found")
        print("Please install pip: https://pip.pypa.io/en/stable/installation/")
        return False

def get_system_info():
    """Get system information"""
    print("\n💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {sys.version}")
    
    return {
        'os': platform.system(),
        'architecture': platform.machine(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}"
    }

def install_package(package, description=""):
    """Install a single package with error handling"""
    try:
        print(f"   Installing {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package, "--upgrade"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"   ✅ {package} installed successfully")
            return True
        else:
            print(f"   ❌ Failed to install {package}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout installing {package}")
        return False
    except Exception as e:
        print(f"   ❌ Error installing {package}: {e}")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("\n📦 Installing Dependencies...")
    
    # Core dependencies
    core_deps = [
        ("pyserial>=3.5", "Serial communication"),
        ("numpy>=1.24.0", "Numerical computations"),
        ("requests>=2.28.0", "HTTP requests"),
        ("python-dotenv>=1.0.0", "Environment variables")
    ]
    
    # GUI dependencies
    gui_deps = [
        ("customtkinter>=5.2.0", "Modern GUI framework"),
        ("matplotlib>=3.7.0", "Data plotting"),
        ("Pillow>=10.0.0", "Image processing"),
        ("psutil>=5.9.0", "Performance monitoring")
    ]
    
    # Legacy GUI dependencies (optional)
    legacy_deps = [
        ("PyQt5>=5.15.0", "Legacy GUI framework"),
        ("pyqtgraph>=0.13.0", "Legacy plotting")
    ]
    
    print("📋 Core Dependencies:")
    core_success = all(install_package(pkg, desc) for pkg, desc in core_deps)
    
    print("\\n🎨 Modern GUI Dependencies:")
    gui_success = all(install_package(pkg, desc) for pkg, desc in gui_deps)
    
    print("\\n📱 Legacy GUI Dependencies (optional):")
    legacy_success = True  # Don't require these
    for pkg, desc in legacy_deps:
        try:
            install_package(pkg, desc)
        except:
            print(f"   ⚠️  {pkg} - optional dependency failed (continuing)")
    
    return core_success and gui_success

def check_installation():
    """Verify installation by importing modules"""
    print("\\n🔍 Verifying Installation...")
    
    modules_to_check = {
        'customtkinter': 'Modern GUI framework',
        'matplotlib': 'Data plotting',
        'numpy': 'Numerical computations', 
        'serial': 'Serial communication (pyserial)',
        'requests': 'HTTP requests',
        'psutil': 'Performance monitoring',
        'PIL': 'Image processing (Pillow)'
    }
    
    success_count = 0
    for module, description in modules_to_check.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {module} - {description}")
            success_count += 1
        except ImportError:
            print(f"   ❌ {module} - {description} (FAILED)")
    
    print(f"\\n📊 Installation Status: {success_count}/{len(modules_to_check)} modules verified")
    return success_count == len(modules_to_check)

def create_desktop_shortcut():
    """Create desktop shortcut (if possible)"""
    try:
        system_info = platform.system()
        project_dir = Path(__file__).parent.absolute()
        
        if system_info == "Windows":
            # Windows shortcut creation
            shortcut_path = Path.home() / "Desktop" / "ECG AI Heart Diagnosis.bat"
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\\ncd /d "{project_dir}"\\npython launch_modern_gui.py\\npause')
            print(f"   ✅ Windows shortcut created: {shortcut_path}")
            
        elif system_info == "Linux":
            # Linux desktop entry
            shortcut_path = Path.home() / ".local/share/applications/ecg-ai-diagnosis.desktop"
            shortcut_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(shortcut_path, 'w') as f:
                f.write(f"""[Desktop Entry]
Name=ECG AI Heart Diagnosis
Comment=Modern ECG monitoring with AI diagnosis
Exec=python3 {project_dir}/launch_modern_gui.py
Path={project_dir}
Icon={project_dir}/assets/icon.png
Terminal=false
Type=Application
Categories=Science;MedicalSoftware;
""")
            print(f"   ✅ Linux desktop entry created: {shortcut_path}")
            
        return True
    except Exception as e:
        print(f"   ⚠️  Could not create desktop shortcut: {e}")
        return False

def run_quick_test():
    """Run a quick functionality test"""
    print("\\n🧪 Running Quick Test...")
    
    try:
        # Test circular buffer
        sys.path.append('ecg_receiver/core')
        from circular_buffer import CircularECGBuffer
        
        buffer = CircularECGBuffer(100)
        buffer.append([1, 2, 3, 4, 5])
        data = buffer.get_recent_data(3)
        
        if len(data) == 3:
            print("   ✅ Circular buffer working")
        else:
            print("   ❌ Circular buffer test failed")
            return False
            
        # Test performance monitor
        from performance_monitor import PerformanceMonitor
        monitor = PerformanceMonitor()
        report = monitor.get_performance_report()
        
        if 'cpu_percent' in report:
            print("   ✅ Performance monitor working")
        else:
            print("   ❌ Performance monitor test failed")
            return False
            
        print("   ✅ All core components functional")
        return True
        
    except Exception as e:
        print(f"   ❌ Quick test failed: {e}")
        return False

def print_completion_info():
    """Print completion information and usage instructions"""
    print("\\n🎉 Installation Complete!")
    print("=" * 60)
    print("\\n🚀 How to Launch the Application:")
    print("   Option 1 (Modern GUI): python launch_modern_gui.py")
    print("   Option 2 (Legacy GUI):  python -m ecg_receiver.main")
    print("\\n📋 What's Included:")
    print("   ✅ Modern CustomTkinter GUI with medical-grade design")
    print("   ✅ AI-powered heart diagnosis with Gemini 2.5 Flash")
    print("   ✅ Real-time ECG plotting with performance optimizations")
    print("   ✅ Memory-efficient circular buffer system")
    print("   ✅ Performance monitoring and metrics")
    print("   ✅ Cross-platform compatibility (Windows, Linux, macOS)")
    print("\\n⚙️  Configuration:")
    print("   • Set up your Gemini API key in the GUI")
    print("   • Connect ESP32 + ADS1292R ECG hardware via USB")
    print("   • Select appropriate serial port in application")
    print("\\n📚 Documentation:")
    print("   • PERFORMANCE_OPTIMIZATION_REPORT.md - Performance details")
    print("   • TKINTER_DESIGNER_GUIDE.md - GUI customization guide")
    print("   • README.md - Complete project documentation")
    print("\\n❤️  Ready for ECG AI Heart Diagnosis!")

def main():
    """Main installation function"""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Get system info
    system_info = get_system_info()
    
    # Install dependencies
    print("\\nStarting installation process...")
    if not install_dependencies():
        print("\\n❌ Installation failed. Please check errors above.")
        sys.exit(1)
    
    # Verify installation
    if not check_installation():
        print("\\n⚠️  Installation completed with some issues.")
        print("You may still be able to run the application.")
    
    # Create shortcuts
    print("\\n🔗 Creating Shortcuts...")
    create_desktop_shortcut()
    
    # Run quick test
    if run_quick_test():
        print("\\n✅ All systems operational!")
    else:
        print("\\n⚠️  Some functionality may be limited.")
    
    # Print completion info
    print_completion_info()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\n\\n❌ Installation error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)