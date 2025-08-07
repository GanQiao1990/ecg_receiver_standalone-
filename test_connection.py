#!/usr/bin/env python3
"""
Test script for ECG receiver connection functionality.
This script tests the serial connection and data parsing without GUI.
"""

import sys
import time
import signal
from ecg_receiver.core.serial_handler import SerialHandler

class ECGTester:
    def __init__(self):
        self.serial_handler = SerialHandler()
        self.running = True
        self.packet_count = 0
        self.start_time = time.time()
        
    def handle_data(self, data):
        """Handle received data."""
        self.packet_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        print(f"[{elapsed:.2f}s] Packet {self.packet_count}: {data}")
        
        # Parse ECG data if available
        if data.startswith('DATA,'):
            try:
                parts = data.split(',')
                if len(parts) >= 4:
                    ecg_value = float(parts[2])
                    print(f"  -> ECG Value: {ecg_value} μV")
            except (ValueError, IndexError) as e:
                print(f"  -> Parse Error: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print("\nShutting down...")
        self.running = False
        self.serial_handler.disconnect()
        sys.exit(0)
    
    def run_test(self):
        """Run the connection test."""
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("ECG Receiver Connection Test")
        print("=" * 40)
        
        # List available ports
        ports = self.serial_handler.list_ports()
        if not ports:
            print("No serial ports found!")
            return False
        
        print(f"Available ports: {', '.join(ports)}")
        
        # Try to connect to the first available port
        # In a real scenario, you might want to specify the port
        test_port = ports[0]
        print(f"\nAttempting to connect to {test_port}...")
        
        if not self.serial_handler.connect(test_port):
            print(f"Failed to connect to {test_port}")
            return False
        
        print(f"Successfully connected to {test_port}")
        print("Starting data collection... (Press Ctrl+C to stop)")
        
        # Start reading data
        if not self.serial_handler.start_reading(self.handle_data):
            print("Failed to start reading data")
            return False
        
        # Keep the test running
        try:
            while self.running:
                time.sleep(1)
                
                # Print statistics every 10 seconds
                elapsed = time.time() - self.start_time
                if int(elapsed) % 10 == 0 and elapsed > 1:
                    rate = self.packet_count / elapsed
                    print(f"\nStatistics: {self.packet_count} packets in {elapsed:.1f}s (Rate: {rate:.2f} Hz)")
                    
        except KeyboardInterrupt:
            pass
        
        # Cleanup
        self.serial_handler.disconnect()
        print("\nTest completed.")
        return True

def main():
    """Main function."""
    tester = ECGTester()
    success = tester.run_test()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())