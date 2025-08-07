"""
Main window for the ECG Receiver application with heart diagnosis functionality.
"""

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, 
                           QHBoxLayout, QLabel, QMessageBox, QTextEdit, QGroupBox, 
                           QLineEdit, QFormLayout, QTabWidget, QScrollArea, QSplitter)
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QThread, Qt
from PyQt5.QtGui import QFont, QColor
import pyqtgraph as pg
import numpy as np
import time
from datetime import datetime
import os
import json
from typing import Optional, Dict, Any

from ..core.serial_handler import SerialHandler
from ..core.data_recorder import DataRecorder

# Import diagnosis client using absolute import to avoid relative import issues
try:
    from ecg_diagnosis import GeminiECGDiagnosisClient
except ImportError:
    # Fallback for different import contexts
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from ecg_diagnosis import GeminiECGDiagnosisClient


class DiagnosisWorker(QThread):
    """Worker thread for ECG diagnosis to prevent UI blocking."""
    
    diagnosis_completed = pyqtSignal(dict)
    diagnosis_error = pyqtSignal(str)
    
    def __init__(self, diagnosis_client, ecg_data, patient_info=None):
        super().__init__()
        self.diagnosis_client = diagnosis_client
        self.ecg_data = ecg_data
        self.patient_info = patient_info
    
    def run(self):
        """Run diagnosis in background thread."""
        try:
            processed_data = self.diagnosis_client.preprocess_ecg_data(self.ecg_data)
            diagnosis = self.diagnosis_client.diagnose_heart_condition(processed_data, self.patient_info)
            self.diagnosis_completed.emit(diagnosis)
        except Exception as e:
            self.diagnosis_error.emit(str(e))


class ECGMainWindow(QMainWindow):
    """Main window for the ECG Receiver application with diagnosis functionality."""
    
    # Define signals for thread safety
    data_received = pyqtSignal(str)
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Application state
        self.serial_handler = SerialHandler()
        self.data_recorder = DataRecorder()
        
        # Diagnosis client (will be initialized when API key is provided)
        self.diagnosis_client: Optional[GeminiECGDiagnosisClient] = None
        self.diagnosis_worker: Optional[DiagnosisWorker] = None
        
        # Data buffers - increased size for better visualization
        self.max_points = 2000  # Increased buffer size
        self.time_data = np.zeros(self.max_points)
        self.ecg_data = np.zeros(self.max_points)
        self.pointer = 0
        
        # Store raw ECG values for diagnosis (larger buffer)
        self.diagnosis_buffer_size = 5000  # 20 seconds at 250Hz
        self.raw_ecg_values = []
        
        # Create the time axis (time in seconds, 8 seconds of data)
        self.time_axis = np.linspace(-8, 0, self.max_points)
        
        # Connection state
        self.current_port = None
        self.packets_received = 0
        self.last_packet_time = None
        
        # Diagnosis state
        self.last_diagnosis = None
        self.diagnosis_history = []
        
        # Connect signals
        self.data_received.connect(self.process_data_slot)
        
        # Initialize the UI
        self.init_ui()
        
        # Set up data update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # Update at 20Hz
        
        # Auto-diagnosis timer (every 30 seconds if enabled)
        self.auto_diagnosis_timer = QTimer()
        self.auto_diagnosis_timer.timeout.connect(self.perform_auto_diagnosis)
        self.auto_diagnosis_enabled = False
        
    def init_ui(self):
        """Initialize the user interface with diagnosis functionality."""
        self.setWindowTitle('ECG Real-time Monitor with AI Diagnosis')
        self.setGeometry(100, 100, 1400, 900)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        
        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for ECG visualization
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Control panel
        control_group = QGroupBox("Connection Control")
        control_layout = QVBoxLayout()
        
        # First row: Port selection and connection
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(150)
        port_layout.addWidget(self.port_combo)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        port_layout.addWidget(self.connect_btn)
        
        refresh_btn = QPushButton("Refresh Ports")
        refresh_btn.clicked.connect(self.scan_ports)
        port_layout.addWidget(refresh_btn)
        
        control_layout.addLayout(port_layout)
        
        # Second row: Recording and status
        record_layout = QHBoxLayout()
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.setEnabled(False)
        self.record_btn.clicked.connect(self.toggle_recording)
        record_layout.addWidget(self.record_btn)
        
        self.status_label = QLabel("Status: Disconnected")
        record_layout.addWidget(self.status_label)
        
        control_layout.addLayout(record_layout)
        control_group.setLayout(control_layout)
        left_layout.addWidget(control_group)
        
        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'ECG (μV)')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.plot_widget.setTitle('ECG Waveform')
        self.plot_curve = self.plot_widget.plot(pen='b')
        
        left_layout.addWidget(self.plot_widget)
        left_panel.setLayout(left_layout)
        
        # Right panel for diagnosis
        right_panel = self.create_diagnosis_panel()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 600])  # Set initial sizes
        
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        
        # Initial port scan
        self.scan_ports()
    
    def create_diagnosis_panel(self):
        """Create the diagnosis panel UI."""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # API Configuration
        api_group = QGroupBox("AI Diagnosis Configuration")
        api_layout = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your Gemini API key")
        api_layout.addRow("API Key:", self.api_key_input)
        
        self.api_url_input = QLineEdit("https://api.gptnb.ai/")
        api_layout.addRow("API URL:", self.api_url_input)
        
        config_buttons_layout = QHBoxLayout()
        self.setup_api_btn = QPushButton("Setup API")
        self.setup_api_btn.clicked.connect(self.setup_diagnosis_api)
        config_buttons_layout.addWidget(self.setup_api_btn)
        
        self.api_status_label = QLabel("Status: Not configured")
        config_buttons_layout.addWidget(self.api_status_label)
        
        api_layout.addRow(config_buttons_layout)
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Patient Information
        patient_group = QGroupBox("Patient Information (Optional)")
        patient_layout = QFormLayout()
        
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("e.g., 45")
        patient_layout.addRow("Age:", self.age_input)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Male", "Female", "Other"])
        patient_layout.addRow("Gender:", self.gender_combo)
        
        self.symptoms_input = QLineEdit()
        self.symptoms_input.setPlaceholderText("e.g., chest pain, shortness of breath")
        patient_layout.addRow("Symptoms:", self.symptoms_input)
        
        patient_group.setLayout(patient_layout)
        layout.addWidget(patient_group)
        
        # Diagnosis Controls
        diagnosis_control_group = QGroupBox("Diagnosis Control")
        diagnosis_control_layout = QVBoxLayout()
        
        buttons_layout = QHBoxLayout()
        self.diagnose_btn = QPushButton("Analyze Current ECG")
        self.diagnose_btn.setEnabled(False)
        self.diagnose_btn.clicked.connect(self.start_diagnosis)
        buttons_layout.addWidget(self.diagnose_btn)
        
        self.auto_diagnosis_checkbox = QPushButton("Enable Auto-Diagnosis")
        self.auto_diagnosis_checkbox.setCheckable(True)
        self.auto_diagnosis_checkbox.toggled.connect(self.toggle_auto_diagnosis)
        buttons_layout.addWidget(self.auto_diagnosis_checkbox)
        
        diagnosis_control_layout.addLayout(buttons_layout)
        
        self.diagnosis_status_label = QLabel("Ready for diagnosis")
        diagnosis_control_layout.addWidget(self.diagnosis_status_label)
        
        diagnosis_control_group.setLayout(diagnosis_control_layout)
        layout.addWidget(diagnosis_control_group)
        
        # Diagnosis Results
        results_group = QGroupBox("Diagnosis Results")
        results_layout = QVBoxLayout()
        
        # Create tabbed interface for results
        self.results_tabs = QTabWidget()
        
        # Current diagnosis tab
        self.current_diagnosis_text = QTextEdit()
        self.current_diagnosis_text.setReadOnly(True)
        self.current_diagnosis_text.setMinimumHeight(200)
        self.results_tabs.addTab(self.current_diagnosis_text, "Current Diagnosis")
        
        # History tab
        self.diagnosis_history_text = QTextEdit()
        self.diagnosis_history_text.setReadOnly(True)
        self.results_tabs.addTab(self.diagnosis_history_text, "History")
        
        # Statistics tab
        self.ecg_stats_text = QTextEdit()
        self.ecg_stats_text.setReadOnly(True)
        self.results_tabs.addTab(self.ecg_stats_text, "ECG Statistics")
        
        results_layout.addWidget(self.results_tabs)
        
        # Clear results button
        clear_btn = QPushButton("Clear Results")
        clear_btn.clicked.connect(self.clear_diagnosis_results)
        results_layout.addWidget(clear_btn)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        panel.setLayout(layout)
        return panel
    
    def scan_ports(self):
        """Scan for available serial ports."""
        self.port_combo.clear()
        for port in self.serial_handler.list_ports():
            self.port_combo.addItem(port)
    
    def toggle_connection(self):
        """Connect to or disconnect from the selected serial port."""
        if not self.serial_handler.is_connected:
            port = self.port_combo.currentText()
            if not port:
                self.status_label.setText("Status: No port selected")
                QMessageBox.warning(self, "Connection Error", "Please select a serial port.")
                return
                
            print(f"Attempting to connect to {port}...")
            self.current_port = port
            
            if self.serial_handler.connect(port):
                self.connect_btn.setText("Disconnect")
                self.record_btn.setEnabled(True)
                self.status_label.setText(f"Status: Connected to {port}")
                
                # Reset statistics
                self.packets_received = 0
                
                # Clear previous data
                self.pointer = 0
                self.ecg_data.fill(0)
                
                print(f"Successfully connected to {port}")
                
                # Start the data processing thread with thread-safe callback
                self.serial_handler.start_reading(self.handle_serial_data)
            else:
                self.status_label.setText(f"Status: Connection failed")
                QMessageBox.critical(self, "Connection Error", 
                                   f"Could not connect to {port}.\n\n"
                                   "Please check:\n"
                                   "- Device is connected\n"
                                   "- Port is not in use\n"
                                   "- Device drivers are installed")
        else:
            self.disconnect_serial()
    
    def disconnect_serial(self):
        """Disconnect from the serial port."""
        if self.data_recorder.recording:
            self.stop_recording()
            
        self.serial_handler.disconnect()
        self.connect_btn.setText("Connect")
        self.record_btn.setEnabled(False)
        self.status_label.setText("Status: Disconnected")
    
    def toggle_recording(self):
        """Start or stop recording data to CSV."""
        if not self.data_recorder.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording data to a CSV file."""
        if self.data_recorder.start_recording():
            self.record_btn.setText("Stop Recording")
            self.status_label.setText(f"Status: Recording to {self.data_recorder.current_filename}")
        else:
            self.status_label.setText("Status: Could not start recording")
    
    def stop_recording(self):
        """Stop recording data to CSV."""
        self.data_recorder.stop_recording()
        self.record_btn.setText("Start Recording")
        self.status_label.setText("Status: Connected")
    
    def handle_serial_data(self, data):
        """Handle data received from serial port (called from worker thread)."""
        # Emit signal to handle data in main thread
        self.data_received.emit(data)
    
    @pyqtSlot(str)
    def process_data_slot(self, data):
        """Process data in the main thread (connected to data_received signal)."""
        self.process_data(data)
    
    def process_data(self, data):
        """Process a data line and update the buffers."""
        current_time = time.time()
        self.last_packet_time = current_time
        
        # Handle different data formats
        ecg_value = None
        
        if data.startswith('DATA,'):
            # Standard CSV format: "DATA,timestamp,ecg,resp,hr,status"
            try:
                parts = data.split(',')
                if len(parts) >= 4:  # We need at least timestamp, ecg, resp, hr
                    ecg_value = float(parts[2])
            except (ValueError, IndexError) as e:
                print(f"Error parsing CSV data: {data[:50]}... Error: {e}")
                
        elif data.startswith('ERROR,') or data.startswith('INFO,'):
            # Log system messages
            print(f"Device: {data}")
            return  # Don't process as ECG data
            
        else:
            # Try to parse as simple numeric data
            try:
                data_clean = data.strip()
                
                # Handle single numeric value (like "-7", "-6", "-5")
                if data_clean and (data_clean.replace('-', '').replace('.', '').isdigit() or 
                                   data_clean.replace('-', '').replace('.', '').replace(' ', '').isdigit()):
                    ecg_value = float(data_clean)
                    
                # Handle multiple space/comma separated values
                else:
                    parts = data_clean.replace(',', ' ').split()
                    if 1 <= len(parts) <= 5:  # 1-5 numeric values
                        # Try each part as potential ECG value
                        for part in parts:
                            try:
                                test_value = float(part.strip())
                                # Use the first valid numeric value as ECG
                                if ecg_value is None:
                                    ecg_value = test_value
                                break
                            except ValueError:
                                continue
                                
            except Exception as e:
                # If we can't parse it at all, just log it
                if data.strip():  # Only log non-empty lines
                    print(f"Unknown data format: {data[:50]}...")
                return
        
        # If we successfully extracted an ECG value, process it
        if ecg_value is not None:
            # Update statistics
            self.packets_received += 1
            
            # Update data buffer for visualization
            self.ecg_data[self.pointer] = ecg_value
            self.pointer = (self.pointer + 1) % self.max_points
            
            # Store raw ECG values for diagnosis
            self.raw_ecg_values.append(ecg_value)
            if len(self.raw_ecg_values) > self.diagnosis_buffer_size:
                self.raw_ecg_values.pop(0)  # Remove oldest value
            
            # Save to CSV if recording
            if self.data_recorder.recording:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                self.data_recorder.write_data(timestamp, ecg_value)
                
            # Optional: Print received values for debugging
            if self.packets_received % 50 == 0:  # Print every 50th packet
                print(f"Received ECG value: {ecg_value} (Packet #{self.packets_received})")
                
            # Update ECG statistics display
            if self.packets_received % 100 == 0:  # Update every 100 packets
                self.update_ecg_statistics()
    
    def update_plot(self):
        """Update the plot with new data."""
        if self.pointer == 0:
            return
            
        # Create x-axis data (time in seconds, assuming 200Hz sampling rate)
        x = np.roll(self.time_axis, -self.pointer)
        
        # Get the data in the correct order for plotting
        if self.pointer > 0:
            y = np.concatenate((self.ecg_data[self.pointer:], self.ecg_data[:self.pointer]))
        else:
            y = self.ecg_data
            
        # Update the plot
        self.plot_curve.setData(x, y)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.disconnect_serial()
        
        # Stop any running diagnosis
        if self.diagnosis_worker and self.diagnosis_worker.isRunning():
            self.diagnosis_worker.quit()
            self.diagnosis_worker.wait()
            
        event.accept()
    
    # Diagnosis-related methods
    
    def setup_diagnosis_api(self):
        """Setup the diagnosis API client."""
        api_key = self.api_key_input.text().strip()
        api_url = self.api_url_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "API Setup", "Please enter an API key.")
            return
        
        try:
            self.diagnosis_client = GeminiECGDiagnosisClient(api_key, api_url)
            self.api_status_label.setText("Status: Configured ✓")
            self.api_status_label.setStyleSheet("color: green;")
            self.diagnose_btn.setEnabled(len(self.raw_ecg_values) > 100)
            QMessageBox.information(self, "API Setup", "Diagnosis API configured successfully!")
        except Exception as e:
            self.api_status_label.setText("Status: Configuration failed")
            self.api_status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "API Setup Error", f"Failed to setup API: {str(e)}")
    
    def get_patient_info(self) -> Optional[Dict[str, Any]]:
        """Get patient information from form inputs."""
        patient_info = {}
        
        age = self.age_input.text().strip()
        if age:
            try:
                patient_info['age'] = int(age)
            except ValueError:
                pass
        
        gender = self.gender_combo.currentText()
        if gender:
            patient_info['gender'] = gender.lower()
        
        symptoms = self.symptoms_input.text().strip()
        if symptoms:
            patient_info['symptoms'] = symptoms
        
        return patient_info if patient_info else None
    
    def start_diagnosis(self):
        """Start ECG diagnosis in background thread."""
        if not self.diagnosis_client:
            QMessageBox.warning(self, "Diagnosis", "Please setup the API first.")
            return
        
        if len(self.raw_ecg_values) < 100:
            QMessageBox.warning(self, "Diagnosis", "Not enough ECG data for analysis. Please wait for more data.")
            return
        
        if self.diagnosis_worker and self.diagnosis_worker.isRunning():
            QMessageBox.information(self, "Diagnosis", "Diagnosis already in progress.")
            return
        
        # Get patient information
        patient_info = self.get_patient_info()
        
        # Use last 2500 samples (10 seconds at 250Hz) for diagnosis
        ecg_data_for_diagnosis = self.raw_ecg_values[-2500:] if len(self.raw_ecg_values) >= 2500 else self.raw_ecg_values.copy()
        
        # Start diagnosis worker
        self.diagnosis_worker = DiagnosisWorker(self.diagnosis_client, ecg_data_for_diagnosis, patient_info)
        self.diagnosis_worker.diagnosis_completed.connect(self.on_diagnosis_completed)
        self.diagnosis_worker.diagnosis_error.connect(self.on_diagnosis_error)
        
        # Update UI state
        self.diagnose_btn.setEnabled(False)
        self.diagnosis_status_label.setText("Analyzing ECG data...")
        self.diagnosis_status_label.setStyleSheet("color: blue;")
        
        self.diagnosis_worker.start()
    
    def on_diagnosis_completed(self, diagnosis: Dict[str, Any]):
        """Handle completed diagnosis."""
        self.last_diagnosis = diagnosis
        self.diagnosis_history.append({
            'timestamp': datetime.now().isoformat(),
            'diagnosis': diagnosis
        })
        
        # Update UI
        self.display_diagnosis(diagnosis)
        self.update_diagnosis_history()
        
        # Reset UI state
        self.diagnose_btn.setEnabled(True)
        self.diagnosis_status_label.setText("Diagnosis completed")
        self.diagnosis_status_label.setStyleSheet("color: green;")
    
    def on_diagnosis_error(self, error_message: str):
        """Handle diagnosis error."""
        self.diagnosis_status_label.setText(f"Diagnosis failed: {error_message}")
        self.diagnosis_status_label.setStyleSheet("color: red;")
        self.diagnose_btn.setEnabled(True)
        
        # Show error message
        error_text = f"Diagnosis Error ({datetime.now().strftime('%H:%M:%S')}):\n{error_message}\n\n"
        self.current_diagnosis_text.append(error_text)
    
    def display_diagnosis(self, diagnosis: Dict[str, Any]):
        """Display diagnosis results in the UI."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Format diagnosis text
        diagnosis_text = f"=== ECG DIAGNOSIS REPORT ===\n"
        diagnosis_text += f"Timestamp: {timestamp}\n\n"
        
        # Primary diagnosis
        primary_diagnosis = diagnosis.get('primary_diagnosis', 'Unknown')
        severity = diagnosis.get('severity', 'unknown')
        confidence = diagnosis.get('confidence', 0.0)
        
        diagnosis_text += f"PRIMARY DIAGNOSIS: {primary_diagnosis}\n"
        diagnosis_text += f"SEVERITY: {severity.upper()}\n"
        diagnosis_text += f"CONFIDENCE: {confidence:.1%}\n\n"
        
        # Secondary conditions
        secondary = diagnosis.get('secondary_conditions', [])
        if secondary:
            diagnosis_text += f"POSSIBLE SECONDARY CONDITIONS:\n"
            for condition in secondary:
                diagnosis_text += f"• {condition}\n"
            diagnosis_text += "\n"
        
        # Key findings
        findings = diagnosis.get('key_findings', [])
        if findings:
            diagnosis_text += f"KEY ECG FINDINGS:\n"
            for finding in findings:
                diagnosis_text += f"• {finding}\n"
            diagnosis_text += "\n"
        
        # Recommendations
        recommendations = diagnosis.get('recommendations', {})
        if recommendations:
            diagnosis_text += f"RECOMMENDATIONS:\n"
            
            immediate = recommendations.get('immediate_actions', [])
            if immediate:
                diagnosis_text += f"Immediate Actions:\n"
                for action in immediate:
                    diagnosis_text += f"• {action}\n"
                diagnosis_text += "\n"
            
            follow_up = recommendations.get('follow_up', [])
            if follow_up:
                diagnosis_text += f"Follow-up:\n"
                for item in follow_up:
                    diagnosis_text += f"• {item}\n"
                diagnosis_text += "\n"
            
            lifestyle = recommendations.get('lifestyle', [])
            if lifestyle:
                diagnosis_text += f"Lifestyle:\n"
                for item in lifestyle:
                    diagnosis_text += f"• {item}\n"
                diagnosis_text += "\n"
        
        # Normal ranges comparison
        normal_ranges = diagnosis.get('normal_ranges_comparison', {})
        if normal_ranges:
            diagnosis_text += f"NORMAL RANGES COMPARISON:\n"
            for key, value in normal_ranges.items():
                diagnosis_text += f"• {key.replace('_', ' ').title()}: {value}\n"
            diagnosis_text += "\n"
        
        # Risk factors
        risk_factors = diagnosis.get('risk_factors', [])
        if risk_factors:
            diagnosis_text += f"IDENTIFIED RISK FACTORS:\n"
            for factor in risk_factors:
                diagnosis_text += f"• {factor}\n"
            diagnosis_text += "\n"
        
        # Prognosis
        prognosis = diagnosis.get('prognosis')
        if prognosis:
            diagnosis_text += f"PROGNOSIS: {prognosis}\n\n"
        
        # Set color based on severity
        color = "black"
        if severity.lower() in ['high', 'critical']:
            color = "red"
        elif severity.lower() == 'moderate':
            color = "orange"
        elif severity.lower() == 'low':
            color = "green"
        
        # Display in current diagnosis tab
        self.current_diagnosis_text.clear()
        self.current_diagnosis_text.setStyleSheet(f"color: {color};")
        self.current_diagnosis_text.append(diagnosis_text)
        
        # Switch to diagnosis tab
        self.results_tabs.setCurrentIndex(0)
    
    def update_diagnosis_history(self):
        """Update the diagnosis history display."""
        history_text = ""
        
        for i, entry in enumerate(reversed(self.diagnosis_history[-10:])):  # Show last 10 diagnoses
            timestamp = entry['timestamp']
            diagnosis = entry['diagnosis']
            
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            
            primary = diagnosis.get('primary_diagnosis', 'Unknown')
            severity = diagnosis.get('severity', 'unknown')
            confidence = diagnosis.get('confidence', 0.0)
            
            history_text += f"{i+1}. [{time_str}]\n"
            history_text += f"   Diagnosis: {primary}\n"
            history_text += f"   Severity: {severity}, Confidence: {confidence:.1%}\n\n"
        
        self.diagnosis_history_text.clear()
        self.diagnosis_history_text.append(history_text)
    
    def update_ecg_statistics(self):
        """Update ECG statistics display."""
        if not self.raw_ecg_values:
            return
        
        # Calculate basic statistics
        data = np.array(self.raw_ecg_values)
        
        stats_text = f"=== ECG STATISTICS ===\n"
        stats_text += f"Last Updated: {datetime.now().strftime('%H:%M:%S')}\n\n"
        stats_text += f"Sample Count: {len(self.raw_ecg_values)}\n"
        stats_text += f"Duration: {len(self.raw_ecg_values) / 250:.1f} seconds\n\n"
        stats_text += f"Voltage Statistics:\n"
        stats_text += f"• Mean: {np.mean(data):.2f} μV\n"
        stats_text += f"• Std Dev: {np.std(data):.2f} μV\n"
        stats_text += f"• Min: {np.min(data):.2f} μV\n"
        stats_text += f"• Max: {np.max(data):.2f} μV\n"
        stats_text += f"• Peak-to-Peak: {np.max(data) - np.min(data):.2f} μV\n"
        stats_text += f"• RMS: {np.sqrt(np.mean(data**2)):.2f} μV\n\n"
        
        # Simple peak detection for heart rate estimation
        if len(data) > 500:  # At least 2 seconds of data
            try:
                from ecg_diagnosis import GeminiECGDiagnosisClient
                client = GeminiECGDiagnosisClient("dummy", "dummy")  # Just for preprocessing
                peaks = client._find_peaks(data[-1250:])  # Last 5 seconds
                
                if len(peaks) > 1:
                    peak_intervals = np.diff(peaks) / 250.0  # Convert to seconds
                    if len(peak_intervals) > 0:
                        avg_interval = np.mean(peak_intervals)
                        heart_rate = 60.0 / avg_interval if avg_interval > 0 else 0
                        stats_text += f"Estimated Heart Rate: {heart_rate:.1f} BPM\n"
                        stats_text += f"QRS Complexes Detected: {len(peaks)}\n"
            except ImportError:
                stats_text += "Heart rate estimation unavailable\n"
        
        self.ecg_stats_text.clear()
        self.ecg_stats_text.append(stats_text)
    
    def toggle_auto_diagnosis(self, enabled: bool):
        """Toggle automatic diagnosis."""
        self.auto_diagnosis_enabled = enabled
        
        if enabled and self.diagnosis_client:
            self.auto_diagnosis_timer.start(30000)  # Every 30 seconds
            self.auto_diagnosis_checkbox.setText("Disable Auto-Diagnosis")
            self.diagnosis_status_label.setText("Auto-diagnosis enabled (every 30s)")
        else:
            self.auto_diagnosis_timer.stop()
            self.auto_diagnosis_checkbox.setText("Enable Auto-Diagnosis")
            if not enabled:
                self.diagnosis_status_label.setText("Auto-diagnosis disabled")
    
    def perform_auto_diagnosis(self):
        """Perform automatic diagnosis if conditions are met."""
        if (self.diagnosis_client and len(self.raw_ecg_values) >= 1000 and 
            not (self.diagnosis_worker and self.diagnosis_worker.isRunning())):
            
            print("Performing automatic diagnosis...")
            self.start_diagnosis()
    
    def clear_diagnosis_results(self):
        """Clear all diagnosis results."""
        self.current_diagnosis_text.clear()
        self.diagnosis_history_text.clear()
        self.ecg_stats_text.clear()
        self.diagnosis_history.clear()
        self.last_diagnosis = None
        self.diagnosis_status_label.setText("Results cleared")
