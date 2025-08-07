#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Debug Launch Script
Debug version to identify the exact error location
"""

import sys
import os
import traceback

def main():
    """Debug launch for the modern ECG GUI"""
    print("🔍 ECG AI Heart Diagnosis - Debug Mode")
    print("=" * 50)
    
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.abspath(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        print("📋 Step 1: Checking basic imports...")
        import customtkinter as ctk
        print("✅ customtkinter imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
        
        import numpy as np
        print("✅ numpy imported successfully")
        
        print("\\n📋 Step 2: Checking ECG receiver imports...")
        from ecg_receiver.gui_tkinter.styles.colors import *
        print("✅ Colors module imported")
        
        from ecg_receiver.gui_tkinter.components.modern_widgets import *
        print("✅ Modern widgets imported")
        
        print("\\n📋 Step 3: Creating GUI instance...")
        from ecg_receiver.gui_tkinter.main_window_modern import ModernECGMainWindow
        print("✅ ModernECGMainWindow class imported")
        
        print("\\n📋 Step 4: Initializing GUI...")
        app = ModernECGMainWindow()
        print("✅ GUI instance created successfully")
        
        print("\\n📋 Step 5: Starting main loop...")
        app.run()
        
    except Exception as e:
        print(f"\\n❌ Error at step: {e}")
        print("\\n📋 Full Error Details:")
        traceback.print_exc()
        
        # Additional debugging info
        print("\\n🔍 System Information:")
        print(f"Python version: {sys.version}")
        print(f"Platform: {sys.platform}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Python path: {sys.path[:3]}...")  # Show first 3 paths
        
        # Check specific modules
        print("\\n📦 Module Check:")
        modules = ['customtkinter', 'matplotlib', 'numpy', 'tkinter']
        for module in modules:
            try:
                __import__(module)
                print(f"✅ {module}: Available")
            except ImportError as ie:
                print(f"❌ {module}: Missing - {ie}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()