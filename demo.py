#!/usr/bin/env python3
"""
ECG Receiver with AI Heart Diagnosis - Demo Script
This script demonstrates the complete functionality of the enhanced ECG receiver.
"""

import os
import sys
import json
from datetime import datetime

def print_banner():
    """Print application banner."""
    print("=" * 80)
    print("🫀 ECG RECEIVER WITH AI HEART DIAGNOSIS v2.0")
    print("=" * 80)
    print("Real-time ECG monitoring with Gemini 2.5 Flash AI diagnosis")
    print("Developed by: qiao@126.com")
    print("=" * 80)

def check_requirements():
    """Check if all requirements are installed."""
    print("\n📋 CHECKING REQUIREMENTS...")
    
    required_modules = [
        ('numpy', 'numpy'),
        ('PyQt5', 'PyQt5.QtWidgets'),
        ('pyqtgraph', 'pyqtgraph'),
        ('serial', 'serial'),  
        ('requests', 'requests'),
        ('dotenv', 'dotenv')
    ]
    
    missing = []
    for module_name, import_name in required_modules:
        try:
            __import__(import_name)
            print(f"✅ {module_name} - OK")
        except ImportError:
            print(f"❌ {module_name} - MISSING")
            missing.append(module_name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied!")
    return True

def check_project_structure():
    """Check project structure."""
    print("\n📁 CHECKING PROJECT STRUCTURE...")
    
    required_files = [
        'ecg_diagnosis.py',
        'ecg_receiver/__init__.py',
        'ecg_receiver/main.py',
        'ecg_receiver/gui/main_window.py',
        'ecg_receiver/core/serial_handler.py',
        'ecg_receiver/core/data_recorder.py',
        'requirements.txt',
        'setup.py',
        '.env.example'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ Project structure complete!")
    return True

def test_core_functionality():
    """Test core functionality."""
    print("\n🧪 TESTING CORE FUNCTIONALITY...")
    
    try:
        # Test ECG diagnosis module
        from ecg_diagnosis import GeminiECGDiagnosisClient, create_diagnosis_client
        print("✅ ECG diagnosis module imported successfully")
        
        # Test client creation
        client = GeminiECGDiagnosisClient("test_api_key", "https://api.gptnb.ai/")
        print("✅ Diagnosis client created successfully")
        
        # Test data preprocessing
        sample_data = [100, 102, 105, 110, 150, 120, 100, 95, 98] * 100
        processed = client.preprocess_ecg_data(sample_data)
        print("✅ ECG data preprocessing working")
        
        # Test GUI components
        from ecg_receiver.gui.main_window import ECGMainWindow, DiagnosisWorker
        print("✅ GUI components imported successfully")
        
        # Test main application
        from ecg_receiver.main import main
        print("✅ Application entry point ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {str(e)}")
        return False

def show_feature_summary():
    """Show feature summary."""
    print("\n🚀 FEATURE SUMMARY:")
    print("=" * 50)
    
    features = [
        "🫀 Real-time ECG monitoring and visualization",
        "🤖 AI-powered heart diagnosis using Gemini 2.5 Flash",
        "📊 Comprehensive ECG analysis and statistics",  
        "👥 Patient information integration",
        "📈 Heart rate and rhythm analysis",
        "⚠️  Severity assessment with color coding",
        "🔄 Auto-diagnosis mode (every 30 seconds)",
        "📋 Diagnosis history and tracking",
        "💾 ECG data recording to CSV files",
        "🔧 Enhanced GUI with tabbed diagnosis panel",
        "📡 ESP32 + ADS1292R hardware support",
        "🌐 Cross-platform support (Windows, macOS, Linux)"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n💡 DIAGNOSIS CAPABILITIES:")
    print("  • Arrhythmia detection")
    print("  • Tachycardia and bradycardia identification")  
    print("  • Heart rate variability analysis")
    print("  • QRS complex morphology assessment")
    print("  • Clinical recommendations generation")
    print("  • Risk factor identification")

def show_usage_instructions():
    """Show usage instructions."""
    print("\n📖 QUICK START GUIDE:")
    print("=" * 50)
    
    steps = [
        "1. 🔑 Get Gemini API key from https://api.gptnb.ai/",
        "2. ⚙️  Create .env file: cp .env.example .env",
        "3. 📝 Edit .env and add your API key",
        "4. 🔌 Connect ESP32 with ADS1292R to computer",
        "5. 🚀 Launch: python -m ecg_receiver.main",
        "6. 🔧 Setup API in the diagnosis panel",
        "7. 📡 Connect to ECG device",
        "8. 🫀 Start receiving and analyzing ECG data!"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print("\n🧪 TESTING WITHOUT HARDWARE:")
    print("  • Run: python test_diagnosis.py")
    print("  • This tests the AI diagnosis with simulated ECG data")

def show_api_setup():
    """Show API setup information."""
    print("\n🔑 API CONFIGURATION:")
    print("=" * 50)
    print("Model: Gemini 2.5 Flash Preview (gemini-2.5-flash-preview-04-17)")
    print("Endpoint: https://api.gptnb.ai/")
    print("Features: Heart diagnosis, ECG analysis, clinical recommendations")
    print("")
    print("Required .env configuration:")
    print("  GEMINI_API_KEY=your_api_key_here")
    print("  GEMINI_API_URL=https://api.gptnb.ai/")

def main():
    """Main demo function."""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install missing requirements and try again.")
        return 1
    
    # Check project structure  
    if not check_project_structure():
        print("\n❌ Project structure is incomplete.")
        return 1
    
    # Test functionality
    if not test_core_functionality():
        print("\n❌ Core functionality tests failed.")
        return 1
    
    # Show features and usage
    show_feature_summary()
    show_usage_instructions()
    show_api_setup()
    
    print("\n🎉 ECG RECEIVER WITH AI DIAGNOSIS IS READY!")
    print("=" * 80)
    print("The system has been successfully enhanced with AI heart diagnosis capabilities.")
    print("You can now launch the application and start diagnosing heart conditions!")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())