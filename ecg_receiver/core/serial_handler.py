"""
Serial communication handler for the ECG Receiver application.
"""

import serial
import serial.tools.list_ports
import threading
import time
import queue
from collections import deque

class SerialHandler:
    """Handles serial communication with the ESP32."""
    
    def __init__(self, baudrate=57600):
        """Initialize the serial handler."""
        self.serial_port = None
        self.is_connected = False
        self.baudrate = baudrate
        self.reading_thread = None
        self.stop_thread = False
        self.data_queue = queue.Queue(maxsize=1000)
        self.connection_lock = threading.Lock()
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
    
    def list_ports(self):
        """List available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port):
        """Connect to the specified serial port.
        
        Args:
            port (str): The serial port to connect to.
            
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        with self.connection_lock:
            try:
                # Try multiple connection attempts with different configurations
                for timeout in [2, 5, 10]:  # Try different timeouts
                    try:
                        if self.serial_port:
                            self.serial_port.close()
                        
                        self.serial_port = serial.Serial(
                            port=port,
                            baudrate=self.baudrate,
                            timeout=timeout,
                            write_timeout=timeout,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            rtscts=False,
                            dsrdtr=False
                        )
                        
                        # Wait a moment for the connection to stabilize
                        time.sleep(0.5)
                        
                        # Test the connection by clearing buffers
                        self.serial_port.reset_input_buffer()
                        self.serial_port.reset_output_buffer()
                        
                        self.is_connected = True
                        self.reconnect_attempts = 0
                        print(f"Connected to {port} at {self.baudrate} baud (timeout: {timeout}s)")
                        return True
                        
                    except Exception as inner_e:
                        print(f"Connection attempt failed with timeout {timeout}s: {inner_e}")
                        continue
                        
                print(f"All connection attempts failed for {port}")
                self.is_connected = False
                return False
                
            except Exception as e:
                print(f"Error connecting to {port}: {e}")
                self.is_connected = False
                return False
    
    def disconnect(self):
        """Disconnect from the serial port."""
        with self.connection_lock:
            # Stop the reading thread if it's running
            if self.reading_thread and self.reading_thread.is_alive():
                self.stop_thread = True
                self.reading_thread.join(timeout=2.0)
            
            # Close the serial port
            if self.serial_port and hasattr(self.serial_port, 'is_open') and self.serial_port.is_open:
                try:
                    self.serial_port.close()
                    print("Disconnected from serial port")
                except Exception as e:
                    print(f"Error closing serial port: {e}")
            
            self.is_connected = False
            self.serial_port = None
            
            # Clear the data queue
            while not self.data_queue.empty():
                try:
                    self.data_queue.get_nowait()
                except queue.Empty:
                    break
    
    def start_reading(self, callback):
        """Start reading data from the serial port in a separate thread.
        
        Args:
            callback (callable): Function to call with each line of data.
        """
        if not self.is_connected:
            print("Cannot start reading: not connected")
            return False
        
        # Stop any existing thread
        if self.reading_thread and self.reading_thread.is_alive():
            self.stop_thread = True
            self.reading_thread.join(timeout=1.0)
            
        # Reset thread control flag
        self.stop_thread = False
        
        # Start a new thread
        self.reading_thread = threading.Thread(
            target=self._read_serial_data,
            args=(callback,),
            daemon=True
        )
        self.reading_thread.start()
        return True
    
    def _read_serial_data(self, callback):
        """Read data from the serial port in a separate thread.
        
        Args:
            callback (callable): Function to call with each line of data.
        """
        buffer = ""
        last_data_time = time.time()
        consecutive_errors = 0
        max_consecutive_errors = 10
        
        print("Starting serial data reading thread")
        
        while not self.stop_thread and self.is_connected:
            try:
                # Check if serial port is still valid
                if not self.serial_port or not hasattr(self.serial_port, 'is_open') or not self.serial_port.is_open:
                    print("Serial port is not open, attempting to reconnect...")
                    if not self._attempt_reconnect():
                        break
                    continue
                
                # Read available data with timeout handling
                try:
                    if self.serial_port.in_waiting > 0:
                        raw_data = self.serial_port.read(self.serial_port.in_waiting)
                        if raw_data:
                            # Try different decodings
                            decoded_data = None
                            for encoding in ['ascii', 'utf-8', 'latin-1']:
                                try:
                                    decoded_data = raw_data.decode(encoding, errors='ignore')
                                    break
                                except UnicodeDecodeError:
                                    continue
                            
                            if decoded_data:
                                buffer += decoded_data
                                last_data_time = time.time()
                                consecutive_errors = 0
                                
                                # Process complete lines
                                while '\n' in buffer:
                                    line, buffer = buffer.split('\n', 1)
                                    line = line.strip()
                                    if line and callback:
                                        # Validate data format before calling callback
                                        if self._validate_data_line(line):
                                            try:
                                                callback(line)
                                            except Exception as cb_e:
                                                print(f"Callback error: {cb_e}")
                                        else:
                                            print(f"Invalid data format: {line[:50]}...")  # Show first 50 chars
                    else:
                        # No data available, sleep briefly
                        time.sleep(0.001)  # 1ms sleep
                        
                except serial.SerialTimeoutException:
                    print("Serial timeout occurred")
                    time.sleep(0.1)
                    continue
                except serial.SerialException as se:
                    print(f"Serial exception: {se}")
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        print("Too many consecutive errors, disconnecting")
                        break
                    time.sleep(0.1)
                    continue
                
                # Check for data timeout (5 seconds without data)
                if time.time() - last_data_time > 5:
                    print("Warning: No data received for 5 seconds")
                    # Try to send a test command to check connection
                    if not self._test_connection():
                        print("Connection appears to be lost")
                        break
                    last_data_time = time.time()  # Reset timeout
                    
            except Exception as e:
                consecutive_errors += 1
                print(f"Error reading serial data: {e}")
                if consecutive_errors >= max_consecutive_errors:
                    print("Too many consecutive errors, stopping read thread")
                    break
                time.sleep(0.1)
        
        print("Serial data reading thread stopped")
        self.is_connected = False
    
    def _validate_data_line(self, line):
        """Validate that a data line has the expected format.
        
        Args:
            line (str): The data line to validate.
            
        Returns:
            bool: True if the line appears to be valid ECG data.
        """
        if not line:
            return False
            
        # Check for expected CSV data format: "DATA,timestamp,ecg,resp,hr,status"
        if line.startswith('DATA,'):
            parts = line.split(',')
            if len(parts) >= 4:  # At least DATA, timestamp, ecg, resp
                try:
                    # Try to parse the ECG value
                    float(parts[2])
                    return True
                except (ValueError, IndexError):
                    return False
        
        # Allow other message types (INFO, ERROR, etc.)
        if any(line.startswith(prefix) for prefix in ['INFO,', 'ERROR,', 'STATUS,', 'DEBUG,']):
            return True
        
        # Check for simple numeric data (like "-7", "-6", "-5")
        line = line.strip()
        if line and (line.replace('-', '').replace('.', '').isdigit() or 
                     line.replace('-', '').replace('.', '').replace(' ', '').isdigit()):
            try:
                float(line)
                return True
            except ValueError:
                pass
        
        # Check for space or comma separated numeric values
        parts = line.replace(',', ' ').split()
        if len(parts) >= 1 and len(parts) <= 5:  # 1-5 numeric values
            try:
                for part in parts:
                    float(part.strip())
                return True
            except ValueError:
                pass
            
        return False
    
    def _test_connection(self):
        """Test if the serial connection is still working.
        
        Returns:
            bool: True if connection is working, False otherwise.
        """
        try:
            if self.serial_port and hasattr(self.serial_port, 'is_open') and self.serial_port.is_open:
                # Try to read any available data
                self.serial_port.timeout = 0.1
                test_data = self.serial_port.read(1)
                return True
            return False
        except Exception:
            return False
    
    def _attempt_reconnect(self):
        """Attempt to reconnect to the serial port.
        
        Returns:
            bool: True if reconnection was successful, False otherwise.
        """
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            print(f"Maximum reconnection attempts ({self.max_reconnect_attempts}) reached")
            return False
        
        self.reconnect_attempts += 1
        print(f"Reconnection attempt {self.reconnect_attempts}/{self.max_reconnect_attempts}")
        
        # Try to reconnect (this would need the original port name)
        # For now, just return False to indicate reconnection failed
        # In a real implementation, you'd store the port name and retry connection
        return False
