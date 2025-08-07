#!/usr/bin/env python3
"""
Comprehensive diagnostic script for ECG receiver issues.
This script will help identify and fix connection problems.
"""

import sys
import os
import time
import traceback

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("=== Checking Dependencies ===")
    
    required_packages = {
        'serial': 'pyserial',
        'PyQt5': 'PyQt5', 
        'pyqtgraph': 'pyqtgraph',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            if package == 'serial':
                import serial
                print(f"✓ {pip_name} ({serial.__version__}) - OK")
            elif package == 'PyQt5':
                import PyQt5
                print(f"✓ {pip_name} ({PyQt5.QtCore.PYQT_VERSION_STR}) - OK")
            elif package == 'pyqtgraph':
                import pyqtgraph as pg
                print(f"✓ {pip_name} ({pg.__version__}) - OK")
            elif package == 'numpy':
                import numpy as np
                print(f"✓ {pip_name} ({np.__version__}) - OK")
        except ImportError as e:
            print(f"✗ {pip_name} - MISSING")
            missing_packages.append(pip_name)
            print(f"  Error: {e}")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        return False
    
    print("All dependencies are installed!")
    return True

def check_serial_ports():
    """Check available serial ports."""
    print("\n=== Checking Serial Ports ===")
    
    try:
        import serial.tools.list_ports
        
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:
            print("No serial ports found!")
            print("Possible causes:")
            print("- ESP32 not connected")
            print("- USB drivers not installed")
            print("- Permission issues (Linux: add user to dialout group)")
            return []
        
        print(f"Found {len(ports)} serial ports:")
        
        for i, port in enumerate(ports):
            print(f"{i+1}. {port.device}")
            print(f"   Description: {port.description}")
            print(f"   Hardware ID: {port.hwid}")
            
            # Try to identify ESP32 devices
            if any(keyword in port.description.lower() for keyword in ['esp32', 'cp210', 'ch340', 'ftdi']):
                print("   *** This looks like an ESP32 device! ***")
        
        return [port.device for port in ports]
        
    except Exception as e:
        print(f"Error checking serial ports: {e}")
        return []

def test_serial_connection(port, baudrates=[57600, 115200, 9600]):
    """Test serial connection with different baud rates."""
    print(f"\n=== Testing Connection to {port} ===")
    
    try:
        import serial
        
        for baudrate in baudrates:
            print(f"Trying baudrate {baudrate}...")
            
            try:
                # Test connection
                ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    timeout=2,
                    write_timeout=2
                )
                
                print(f"✓ Connected at {baudrate} baud")
                
                # Try to read some data
                print("Reading data for 5 seconds...")
                start_time = time.time()
                data_received = False
                
                while time.time() - start_time < 5:
                    if ser.in_waiting > 0:
                        try:
                            data = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                            if data.strip():
                                print(f"Received: {data.strip()[:100]}...")
                                data_received = True
                        except Exception as e:
                            print(f"Error reading data: {e}")
                    time.sleep(0.1)
                
                ser.close()
                
                if data_received:
                    print(f"✓ Successfully received data at {baudrate} baud")
                    return baudrate
                else:
                    print(f"⚠ Connected but no data received at {baudrate} baud")
                    
            except serial.SerialException as e:
                print(f"✗ Failed to connect at {baudrate} baud: {e}")
            except Exception as e:
                print(f"✗ Unexpected error at {baudrate} baud: {e}")
        
        print("Could not establish working connection at any baud rate")
        return None
        
    except ImportError:
        print("pyserial not available")
        return None

def test_ecg_data_format():
    """Test ECG data format parsing."""
    print("\n=== Testing ECG Data Format ===")
    
    test_data = [
        "DATA,1234567890,1024,512,75,OK",
        "DATA,1234567891,1050,520,76,OK", 
        "INFO,System started",
        "ERROR,Sensor disconnected",
        "DATA,invalid,data,format",
        "GARBAGE_DATA_123"
    ]
    
    try:
        for data in test_data:
            print(f"Testing: {data}")
            
            if data.startswith('DATA,'):
                try:
                    parts = data.split(',')
                    if len(parts) >= 4:
                        ecg_value = float(parts[2])
                        print(f"  ✓ Valid ECG data: {ecg_value} μV")
                    else:
                        print(f"  ✗ Invalid format: not enough parts")
                except (ValueError, IndexError) as e:
                    print(f"  ✗ Parse error: {e}")
            elif data.startswith(('INFO,', 'ERROR,')):
                print(f"  ✓ Valid system message")
            else:
                print(f"  ⚠ Unknown format")
    
    except Exception as e:
        print(f"Error in data format test: {e}")

def test_gui_components():
    """Test GUI components."""
    print("\n=== Testing GUI Components ===")
    
    try:
        # Test if we can create a QApplication
        from PyQt5.QtWidgets import QApplication
        import sys
        
        # Check if QApplication already exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            created_app = True
        else:
            created_app = False
        
        print("✓ QApplication created successfully")
        
        # Test ECG main window import
        from ecg_receiver.gui.main_window import ECGMainWindow
        print("✓ ECGMainWindow import successful")
        
        # Test creating the window (but don't show it)
        window = ECGMainWindow()
        print("✓ ECGMainWindow created successfully")
        
        # Clean up
        if created_app:
            app.quit()
        
        return True
        
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function."""
    print("ECG Receiver Diagnostic Tool")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and run again.")
        return 1
    
    # Check serial ports
    ports = check_serial_ports()
    
    if ports:
        # Test connection to first available port that looks like ESP32
        esp32_ports = []
        for port in ports:
            # Try to identify ESP32-like ports
            try:
                import serial.tools.list_ports
                port_info = next((p for p in serial.tools.list_ports.comports() if p.device == port), None)
                if port_info and any(keyword in port_info.description.lower() 
                                   for keyword in ['esp32', 'cp210', 'ch340', 'ftdi', 'usb']):
                    esp32_ports.append(port)
            except:
                pass
        
        test_ports = esp32_ports if esp32_ports else ports[:1]  # Test first port if no ESP32 found
        
        for port in test_ports:
            working_baudrate = test_serial_connection(port)
            if working_baudrate:
                print(f"\n✓ Found working connection: {port} at {working_baudrate} baud")
                break
    
    # Test data format parsing
    test_ecg_data_format()
    
    # Test GUI components (only if not in headless environment)
    if os.environ.get('DISPLAY') or sys.platform.startswith('win'):
        test_gui_components()
    else:
        print("\n=== Skipping GUI Test (No Display) ===")
    
    print("\n=== Diagnostic Complete ===")
    print("\nCommon Solutions:")
    print("1. Make sure ESP32 is connected and drivers are installed")
    print("2. Check that ESP32 is sending data in correct format:")
    print("   DATA,timestamp,ecg_value,resp_value,heart_rate,status")
    print("3. Try different baud rates (57600, 115200)")
    print("4. On Linux, add user to dialout group: sudo usermod -a -G dialout $USER")
    print("5. Close other programs that might be using the serial port")

if __name__ == "__main__":
    sys.exit(main())