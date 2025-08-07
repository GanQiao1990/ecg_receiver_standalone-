#!/usr/bin/env python3
"""
Data format analyzer and converter for ECG receiver.
This script helps understand what format your ESP32 is sending.
"""

import serial
import serial.tools.list_ports
import time
import sys

def analyze_data_format(port='COM7', baudrate=57600, duration=10):
    """Analyze the data format being sent by the ESP32."""
    
    print(f"Analyzing data format from {port} at {baudrate} baud for {duration} seconds...")
    print("=" * 60)
    
    try:
        # Connect to serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port}")
        
        start_time = time.time()
        line_count = 0
        valid_numeric_lines = 0
        sample_lines = []
        
        while time.time() - start_time < duration:
            if ser.in_waiting > 0:
                try:
                    # Read line
                    line = ser.readline().decode('ascii', errors='ignore').strip()
                    
                    if line:
                        line_count += 1
                        
                        # Store first 10 lines as samples
                        if len(sample_lines) < 10:
                            sample_lines.append(line)
                        
                        # Check if it's numeric data
                        try:
                            # Try to parse as single number
                            float(line.replace(' ', ''))
                            valid_numeric_lines += 1
                        except ValueError:
                            # Try to parse as multiple numbers
                            parts = line.replace(',', ' ').split()
                            numeric_parts = 0
                            for part in parts:
                                try:
                                    float(part.strip())
                                    numeric_parts += 1
                                except ValueError:
                                    pass
                            
                            if numeric_parts > 0:
                                valid_numeric_lines += 1
                        
                        # Print some lines in real-time
                        if line_count <= 20:
                            print(f"Line {line_count:2d}: '{line}'")
                
                except Exception as e:
                    print(f"Error reading line: {e}")
            
            time.sleep(0.01)
        
        ser.close()
        
        # Analysis results
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS:")
        print(f"Total lines received: {line_count}")
        print(f"Lines with numeric data: {valid_numeric_lines}")
        print(f"Data rate: {line_count/duration:.1f} lines/second")
        
        if line_count > 0:
            print(f"Numeric data percentage: {100*valid_numeric_lines/line_count:.1f}%")
        
        print("\nSample lines:")
        for i, line in enumerate(sample_lines[:10]):
            print(f"  {i+1:2d}: '{line}'")
        
        # Recommendations
        print("\nRECOMMENDations:")
        
        if valid_numeric_lines > 0:
            print("✓ Your ESP32 is sending numeric data!")
            print("✓ The improved ECG receiver should now handle this format.")
            
            # Analyze the format more
            if sample_lines:
                first_line = sample_lines[0]
                
                if ',' in first_line:
                    print("• Data appears to be comma-separated")
                elif ' ' in first_line:
                    print("• Data appears to be space-separated")
                else:
                    print("• Data appears to be single values per line")
                
                # Check if values look like ECG data
                try:
                    test_val = float(first_line.split()[0] if ' ' in first_line 
                                   else first_line.split(',')[0] if ',' in first_line 
                                   else first_line)
                    
                    if -5000 <= test_val <= 5000:
                        print("• Values appear to be in reasonable ECG range")
                    else:
                        print(f"• Values might need scaling (sample: {test_val})")
                        
                except:
                    pass
        else:
            print("✗ No numeric data detected")
            print("• Check your ESP32 code")
            print("• Verify baud rate settings")
            print("• Make sure ESP32 is actually sending ECG data")
        
        return line_count > 0
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def list_available_ports():
    """List all available serial ports."""
    print("Available serial ports:")
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("  No ports found!")
        return []
    
    for i, port in enumerate(ports):
        print(f"  {i+1}. {port.device} - {port.description}")
    
    return [port.device for port in ports]

def main():
    """Main function."""
    print("ECG Data Format Analyzer")
    print("=" * 30)
    
    # List available ports
    ports = list_available_ports()
    
    if not ports:
        print("No serial ports available!")
        return 1
    
    # Use COM7 if available, otherwise first port
    target_port = 'COM7' if 'COM7' in ports else ports[0]
    
    print(f"\nAnalyzing port: {target_port}")
    
    # Analyze the data format
    success = analyze_data_format(target_port)
    
    if success:
        print(f"\n✓ Analysis complete! Your ESP32 on {target_port} is sending data.")
        print("✓ The improved ECG receiver should now work with your data format.")
        print("\nTo test:")
        print("  python -m ecg_receiver.main")
    else:
        print(f"\n✗ Could not analyze data from {target_port}")
        print("• Check connections")
        print("• Verify ESP32 is running and sending data")
        print("• Try different baud rates")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())