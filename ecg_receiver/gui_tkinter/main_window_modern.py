"""
Modern ECG AI Diagnosis GUI - Main Window
Redesigned with CustomTkinter and modern UI principles
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .components.modern_widgets import *
from .styles.colors import *
from ..core.serial_handler import SerialHandler
from ..core.data_recorder import DataRecorder

# Import diagnosis client with fallback
try:
    from ecg_diagnosis import GeminiECGDiagnosisClient
except ImportError:
    # Fallback for different import contexts
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        from ecg_diagnosis import GeminiECGDiagnosisClient
    except ImportError:
        print("Warning: ECG diagnosis module not found")
        GeminiECGDiagnosisClient = None

class DiagnosisWorker:
    """Worker for ECG diagnosis to prevent UI blocking"""
    
    def __init__(self, diagnosis_client, ecg_data, patient_info=None, callback=None, error_callback=None):
        self.diagnosis_client = diagnosis_client
        self.ecg_data = ecg_data
        self.patient_info = patient_info
        self.callback = callback
        self.error_callback = error_callback
    
    def start(self):
        """Start diagnosis in background thread"""
        def run_diagnosis():
            try:
                processed_data = self.diagnosis_client.preprocess_ecg_data(self.ecg_data)
                diagnosis = self.diagnosis_client.diagnose_heart_condition(processed_data, self.patient_info)
                if self.callback:
                    self.callback(diagnosis)
            except Exception as e:
                if self.error_callback:
                    self.error_callback(str(e))
        
        self.thread = threading.Thread(target=run_diagnosis, daemon=True)
        self.thread.start()

class ModernECGMainWindow:
    """Modern ECG AI Diagnosis Main Window"""
    
    def __init__(self):
        """Initialize the modern ECG GUI"""
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize core components
        self.serial_handler = SerialHandler()
        self.data_recorder = DataRecorder()
        self.diagnosis_client: Optional[GeminiECGDiagnosisClient] = None
        self.diagnosis_worker: Optional[DiagnosisWorker] = None
        
        # Data management
        self.raw_ecg_values = []
        self.diagnosis_buffer_size = 5000  # 20 seconds at 250Hz
        self.packets_received = 0
        self.last_diagnosis = None
        self.diagnosis_history = []
        
        # Auto-diagnosis settings
        self.auto_diagnosis_enabled = False
        self.auto_diagnosis_interval = 30  # seconds
        self.last_auto_diagnosis = 0
        
        self.create_main_window()
        self.setup_ui()
        self.setup_data_processing()
        
    def create_main_window(self):
        """Create and configure main window"""
        self.root = ctk.CTk()
        self.root.title("🫀 ECG AI Heart Diagnosis - Modern Interface")
        self.root.geometry(f"{LAYOUT['window_width']}x{LAYOUT['window_height']}")
        self.root.configure(fg_color=BG_DARK)
        
        # Configure window icon and properties
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)
        
        # Center window on screen
        self.center_window()
        
        # Configure closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - LAYOUT['window_width']) // 2
        y = (self.root.winfo_screenheight() - LAYOUT['window_height']) // 2
        self.root.geometry(f"{LAYOUT['window_width']}x{LAYOUT['window_height']}+{x}+{y}")
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container with header and content
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_header()
        self.create_main_content()
        self.create_footer()
    
    def create_header(self):
        """Create modern header with title and controls"""
        self.header_frame = ctk.CTkFrame(
            self.main_container,
            height=LAYOUT["header_height"],
            fg_color=BG_CARD,
            corner_radius=LAYOUT["radius_lg"]
        )
        self.header_frame.pack(fill="x", pady=(0, 10))
        self.header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_header.pack(side="left", fill="y", padx=LAYOUT["padding_lg"])
        
        # App title with icon
        title_label = ctk.CTkLabel(
            left_header,
            text="🫀 ECG AI Heart Diagnosis",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["title"], weight="bold"),
            text_color=TEXT_WHITE
        )
        title_label.pack(side="left", pady=LAYOUT["padding_md"])
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            left_header,
            text="Real-time monitoring with AI-powered diagnosis",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["small"]),
            text_color=TEXT_GRAY
        )
        subtitle_label.pack(side="left", padx=(LAYOUT["padding_md"], 0), pady=LAYOUT["padding_md"])
        
        # Right side - Controls
        right_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_header.pack(side="right", fill="y", padx=LAYOUT["padding_lg"])
        
        # Settings button
        self.settings_btn = ModernButton(
            right_header,
            text="Settings",
            style="secondary",
            icon="settings",
            width=100,
            command=self.open_settings
        )
        self.settings_btn.pack(side="right", padx=(LAYOUT["padding_sm"], 0), pady=LAYOUT["padding_md"])
        
        # Help button
        self.help_btn = ModernButton(
            right_header,
            text="Help",
            style="secondary", 
            icon="help",
            width=80,
            command=self.show_help
        )
        self.help_btn.pack(side="right", pady=LAYOUT["padding_md"])
    
    def create_main_content(self):
        """Create main content area with ECG monitor and diagnosis panels"""
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        
        # Left panel - ECG Monitor
        self.create_ecg_panel()
        
        # Right panel - AI Diagnosis
        self.create_diagnosis_panel()
    
    def create_ecg_panel(self):
        """Create ECG monitoring panel"""
        self.ecg_panel = ModernCard(
            self.content_frame,
            title="ECG Real-time Monitor"
        )
        self.ecg_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ecg_content = self.ecg_panel.get_content_frame()
        
        # ECG Plot
        self.ecg_plot = ECGPlotWidget(ecg_content, height=300)
        self.ecg_plot.pack(fill="both", expand=True, pady=(0, 10))
        
        # Control panel
        self.create_control_panel(ecg_content)
        
        # Statistics panel
        self.create_statistics_panel(ecg_content)
    
    def create_control_panel(self, parent):
        """Create device control panel"""
        control_card = ModernCard(parent, title="Device Control")
        control_card.pack(fill="x", pady=(0, 10))
        
        control_content = control_card.get_content_frame()
        
        # Port selection row
        port_frame = ctk.CTkFrame(control_content, fg_color="transparent")
        port_frame.pack(fill="x", pady=(0, 10))
        
        port_label = ctk.CTkLabel(
            port_frame,
            text="Serial Port:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"]),
            text_color=TEXT_WHITE
        )
        port_label.pack(side="left")
        
        self.port_combo = ctk.CTkComboBox(
            port_frame,
            width=200,
            fg_color=BG_LIGHT,
            button_color=SECONDARY_BLUE,
            button_hover_color=PRIMARY_BLUE,
            text_color=TEXT_WHITE
        )
        self.port_combo.pack(side="left", padx=(10, 0))
        
        # Refresh ports button
        self.refresh_btn = ModernButton(
            port_frame,
            text="Refresh",
            style="secondary",
            icon="refresh",
            width=100,
            command=self.scan_ports
        )
        self.refresh_btn.pack(side="right")
        
        # Connection controls row
        connect_frame = ctk.CTkFrame(control_content, fg_color="transparent")
        connect_frame.pack(fill="x", pady=(0, 10))
        
        # Connect button
        self.connect_btn = ModernButton(
            connect_frame,
            text="Connect",
            style="primary",
            icon="connect",
            width=120,
            command=self.toggle_connection
        )
        self.connect_btn.pack(side="left")
        
        # Record button
        self.record_btn = ModernButton(
            connect_frame,
            text="Start Recording",
            style="success",
            icon="record", 
            width=140,
            state="disabled",
            command=self.toggle_recording
        )
        self.record_btn.pack(side="left", padx=(10, 0))
        
        # Connection status
        self.connection_status = StatusIndicator(connect_frame, status="disconnected")
        self.connection_status.pack(side="right")
    
    def create_statistics_panel(self, parent):
        """Create real-time statistics panel"""
        stats_card = ModernCard(parent, title="Real-time Statistics")
        stats_card.pack(fill="x")
        
        stats_content = stats_card.get_content_frame()
        
        # Statistics grid
        stats_grid = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        # Configure grid
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Heart rate
        hr_frame = ctk.CTkFrame(stats_grid, fg_color=BG_LIGHT, corner_radius=8)
        hr_frame.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        
        ctk.CTkLabel(hr_frame, text="Heart Rate", font=ctk.CTkFont(size=10), text_color=TEXT_GRAY).pack(pady=(5, 0))
        self.hr_label = ctk.CTkLabel(hr_frame, text="-- BPM", font=ctk.CTkFont(size=16, weight="bold"), text_color=SUCCESS_GREEN)
        self.hr_label.pack(pady=(0, 5))
        
        # Signal quality
        quality_frame = ctk.CTkFrame(stats_grid, fg_color=BG_LIGHT, corner_radius=8)
        quality_frame.grid(row=0, column=1, padx=2.5, pady=5, sticky="ew")
        
        ctk.CTkLabel(quality_frame, text="Signal Quality", font=ctk.CTkFont(size=10), text_color=TEXT_GRAY).pack(pady=(5, 0))
        self.quality_label = ctk.CTkLabel(quality_frame, text="--", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_WHITE)
        self.quality_label.pack(pady=(0, 5))
        
        # Data count
        count_frame = ctk.CTkFrame(stats_grid, fg_color=BG_LIGHT, corner_radius=8)
        count_frame.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="ew")
        
        ctk.CTkLabel(count_frame, text="Data Points", font=ctk.CTkFont(size=10), text_color=TEXT_GRAY).pack(pady=(5, 0))
        self.count_label = ctk.CTkLabel(count_frame, text="0", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_WHITE)
        self.count_label.pack(pady=(0, 5))
    
    def create_diagnosis_panel(self):
        """Create AI diagnosis panel"""
        self.diagnosis_panel = ModernCard(
            self.content_frame,
            title="AI Heart Diagnosis"
        )
        self.diagnosis_panel.pack(side="right", fill="both", expand=False, 
                                padx=(5, 0), ipadx=LAYOUT["sidebar_width"]-40)
        
        diagnosis_content = self.diagnosis_panel.get_content_frame()
        
        # API Configuration
        self.create_api_config(diagnosis_content)
        
        # Patient Information
        self.create_patient_info(diagnosis_content)
        
        # Diagnosis Controls
        self.create_diagnosis_controls(diagnosis_content)
        
        # Results Display
        self.create_results_display(diagnosis_content)
    
    def create_api_config(self, parent):
        """Create API configuration section"""
        api_card = ModernCard(parent, title="API Configuration")
        api_card.pack(fill="x", pady=(0, 10))
        
        api_content = api_card.get_content_frame()
        
        # API Key input
        key_frame = ctk.CTkFrame(api_content, fg_color="transparent")
        key_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(key_frame, text="API Key:", text_color=TEXT_WHITE).pack(anchor="w")
        self.api_key_entry = ctk.CTkEntry(
            key_frame,
            placeholder_text="Enter your Gemini API key",
            show="*",
            fg_color=BG_LIGHT,
            border_color=TEXT_GRAY,
            text_color=TEXT_WHITE
        )
        self.api_key_entry.pack(fill="x", pady=(5, 0))
        
        # API URL input  
        url_frame = ctk.CTkFrame(api_content, fg_color="transparent")
        url_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(url_frame, text="API URL:", text_color=TEXT_WHITE).pack(anchor="w")
        self.api_url_entry = ctk.CTkEntry(
            url_frame,
            fg_color=BG_LIGHT,
            border_color=TEXT_GRAY,
            text_color=TEXT_WHITE
        )
        self.api_url_entry.set("https://api.gptnb.ai/")
        self.api_url_entry.pack(fill="x", pady=(5, 0))
        
        # Setup button and status
        setup_frame = ctk.CTkFrame(api_content, fg_color="transparent")
        setup_frame.pack(fill="x")
        
        self.setup_api_btn = ModernButton(
            setup_frame,
            text="Setup API",
            style="primary",
            width=100,
            command=self.setup_diagnosis_api
        )
        self.setup_api_btn.pack(side="left")
        
        self.api_status = StatusIndicator(setup_frame, status="disconnected")
        self.api_status.pack(side="right")
    
    def create_patient_info(self, parent):
        """Create patient information section"""
        patient_card = ModernCard(parent, title="Patient Information")
        patient_card.pack(fill="x", pady=(0, 10))
        
        patient_content = patient_card.get_content_frame()
        
        # Age and Gender row
        info_row1 = ctk.CTkFrame(patient_content, fg_color="transparent")
        info_row1.pack(fill="x", pady=(0, 10))
        
        # Age
        age_frame = ctk.CTkFrame(info_row1, fg_color="transparent")
        age_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(age_frame, text="Age:", text_color=TEXT_WHITE).pack(anchor="w")
        self.age_entry = ctk.CTkEntry(
            age_frame,
            width=80,
            placeholder_text="45",
            fg_color=BG_LIGHT,
            border_color=TEXT_GRAY,
            text_color=TEXT_WHITE
        )
        self.age_entry.pack(fill="x", pady=(5, 0))
        
        # Gender
        gender_frame = ctk.CTkFrame(info_row1, fg_color="transparent")
        gender_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(gender_frame, text="Gender:", text_color=TEXT_WHITE).pack(anchor="w")
        self.gender_combo = ctk.CTkComboBox(
            gender_frame,
            values=["", "Male", "Female", "Other"],
            fg_color=BG_LIGHT,
            button_color=SECONDARY_BLUE,
            text_color=TEXT_WHITE
        )
        self.gender_combo.pack(fill="x", pady=(5, 0))
        
        # Symptoms
        symptoms_frame = ctk.CTkFrame(patient_content, fg_color="transparent")
        symptoms_frame.pack(fill="x")
        
        ctk.CTkLabel(symptoms_frame, text="Symptoms:", text_color=TEXT_WHITE).pack(anchor="w")
        self.symptoms_entry = ctk.CTkEntry(
            symptoms_frame,
            placeholder_text="e.g., chest pain, shortness of breath",
            fg_color=BG_LIGHT,
            border_color=TEXT_GRAY,
            text_color=TEXT_WHITE
        )
        self.symptoms_entry.pack(fill="x", pady=(5, 0))
    
    def create_diagnosis_controls(self, parent):
        """Create diagnosis control section"""
        control_card = ModernCard(parent, title="Diagnosis Control")
        control_card.pack(fill="x", pady=(0, 10))
        
        control_content = control_card.get_content_frame()
        
        # Progress indicator
        self.progress_indicator = ProgressIndicator(control_content)
        
        # Control buttons
        button_frame = ctk.CTkFrame(control_content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))
        
        self.diagnose_btn = ModernButton(
            button_frame,
            text="Analyze ECG",
            style="primary",
            icon="heart",
            state="disabled",
            command=self.start_diagnosis
        )
        self.diagnose_btn.pack(side="left", fill="x", expand=True)
        
        self.auto_diagnosis_btn = ModernButton(
            button_frame,
            text="Auto Mode",
            style="secondary",
            command=self.toggle_auto_diagnosis
        )
        self.auto_diagnosis_btn.pack(side="right", padx=(10, 0))
        
        # Status label
        self.diagnosis_status_label = ctk.CTkLabel(
            control_content,
            text="Ready for diagnosis",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["small"]),
            text_color=TEXT_GRAY
        )
        self.diagnosis_status_label.pack()
    
    def create_results_display(self, parent):
        """Create diagnosis results display"""
        # Tab view for results
        self.results_tabs = ModernTabView(parent)
        self.results_tabs.pack(fill="both", expand=True)
        
        # Current diagnosis tab
        self.results_tabs.add("Current")
        current_tab = self.results_tabs.tab("Current")
        
        self.current_diagnosis_text = ctk.CTkTextbox(
            current_tab,
            font=ctk.CTkFont(family=FONT_FAMILY_MONO, size=FONT_SIZES["small"]),
            fg_color=BG_DARK,
            text_color=TEXT_WHITE
        )
        self.current_diagnosis_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # History tab
        self.results_tabs.add("History")
        history_tab = self.results_tabs.tab("History")
        
        self.history_text = ctk.CTkTextbox(
            history_tab,
            font=ctk.CTkFont(family=FONT_FAMILY_MONO, size=FONT_SIZES["small"]),
            fg_color=BG_DARK,
            text_color=TEXT_WHITE
        )
        self.history_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Statistics tab
        self.results_tabs.add("ECG Stats")
        stats_tab = self.results_tabs.tab("ECG Stats")
        
        self.ecg_stats_text = ctk.CTkTextbox(
            stats_tab,
            font=ctk.CTkFont(family=FONT_FAMILY_MONO, size=FONT_SIZES["small"]),
            fg_color=BG_DARK,
            text_color=TEXT_WHITE
        )
        self.ecg_stats_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_footer(self):
        """Create footer with status information"""
        self.footer_frame = ctk.CTkFrame(
            self.main_container,
            height=LAYOUT["footer_height"],
            fg_color=BG_CARD,
            corner_radius=LAYOUT["radius_md"]
        )
        self.footer_frame.pack(fill="x", pady=(10, 0))
        self.footer_frame.pack_propagate(False)
        
        # Status information
        status_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        status_frame.pack(fill="both", expand=True, padx=LAYOUT["padding_md"])
        
        self.footer_status = ctk.CTkLabel(
            status_frame,
            text="Status: Ready | Heart Rate: -- BPM | Last Diagnosis: Never",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["small"]),
            text_color=TEXT_GRAY
        )
        self.footer_status.pack(side="left", pady=10)
        
        # Version info
        version_label = ctk.CTkLabel(
            status_frame,
            text="ECG AI v2.0",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["tiny"]),
            text_color=TEXT_GRAY
        )
        version_label.pack(side="right", pady=10)
    
    def setup_data_processing(self):
        """Setup data processing and timers"""
        # ECG data processing timer
        self.data_timer = threading.Timer(0.05, self.process_data_queue)  # 20Hz updates
        self.data_timer.daemon = True
        self.data_queue = []
        self.data_lock = threading.Lock()
        
        # Auto-diagnosis timer
        self.auto_diagnosis_timer = threading.Timer(1.0, self.check_auto_diagnosis)
        self.auto_diagnosis_timer.daemon = True
        self.auto_diagnosis_timer.start()
        
        # Statistics update timer
        self.stats_timer = threading.Timer(1.0, self.update_statistics)
        self.stats_timer.daemon = True
        self.stats_timer.start()
        
        # Initial port scan
        self.scan_ports()
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
    
    # Implementation of core functionality methods
    
    def scan_ports(self):
        """Scan for available serial ports"""
        try:
            ports = self.serial_handler.list_ports()
            self.port_combo.configure(values=ports)
            if ports:
                self.port_combo.set(ports[0])
                self.update_footer_status(f"Found {len(ports)} serial ports")
            else:
                self.update_footer_status("No serial ports found")
        except Exception as e:
            self.show_error("Port Scan Error", f"Failed to scan ports: {str(e)}")
    
    def toggle_connection(self):
        """Connect to or disconnect from the selected serial port"""
        if not self.serial_handler.is_connected:
            port = self.port_combo.get()
            if not port:
                self.show_warning("Connection Error", "Please select a serial port.")
                return
            
            self.connect_btn.configure(text="Connecting...", state="disabled")
            self.connection_status.update_status("connecting")
            
            # Connect in background thread
            def connect_thread():
                try:
                    success = self.serial_handler.connect(port)
                    self.root.after(0, self.on_connection_result, success, port)
                except Exception as e:
                    self.root.after(0, self.on_connection_error, str(e))
            
            threading.Thread(target=connect_thread, daemon=True).start()
        else:
            self.disconnect_serial()
    
    def on_connection_result(self, success: bool, port: str):
        """Handle connection result"""
        if success:
            self.connect_btn.configure(text="Disconnect", state="normal")
            self.record_btn.configure(state="normal")
            self.connection_status.update_status("connected")
            
            # Clear previous data
            self.raw_ecg_values.clear()
            self.packets_received = 0
            self.ecg_plot.clear_data()
            
            # Start data processing
            self.serial_handler.start_reading(self.handle_serial_data)
            self.data_timer.start()
            
            self.update_footer_status(f"Connected to {port}")
            self.show_success("Connection Successful", f"Connected to {port}")
        else:
            self.on_connection_error("Connection failed")
    
    def on_connection_error(self, error_msg: str):
        """Handle connection error"""
        self.connect_btn.configure(text="Connect", state="normal")
        self.connection_status.update_status("error")
        self.update_footer_status(f"Connection failed: {error_msg}")
        self.show_error("Connection Error", f"Could not connect to device: {error_msg}")
    
    def disconnect_serial(self):
        """Disconnect from serial port"""
        if self.data_recorder and self.data_recorder.recording:
            self.stop_recording()
        
        self.serial_handler.disconnect()
        self.connect_btn.configure(text="Connect", state="normal")
        self.record_btn.configure(state="disabled")
        self.connection_status.update_status("disconnected")
        self.update_footer_status("Disconnected from device")
    
    def toggle_recording(self):
        """Start or stop recording ECG data"""
        if not self.data_recorder.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording ECG data to CSV file"""
        try:
            if self.data_recorder.start_recording():
                self.record_btn.configure(text="Stop Recording", style="warning")
                filename = self.data_recorder.current_filename
                self.update_footer_status(f"Recording to {filename}")
                self.show_success("Recording Started", f"Recording ECG data to {filename}")
            else:
                self.show_error("Recording Error", "Could not start recording")
        except Exception as e:
            self.show_error("Recording Error", f"Failed to start recording: {str(e)}")
    
    def stop_recording(self):
        """Stop recording ECG data"""
        try:
            self.data_recorder.stop_recording()
            self.record_btn.configure(text="Start Recording", style="success")
            self.update_footer_status("Recording stopped")
        except Exception as e:
            self.show_error("Recording Error", f"Failed to stop recording: {str(e)}")
    
    def setup_diagnosis_api(self):
        """Setup the AI diagnosis API client"""
        api_key = self.api_key_entry.get().strip()
        api_url = self.api_url_entry.get().strip()
        
        if not api_key:
            self.show_warning("API Setup", "Please enter an API key.")
            return
        
        self.setup_api_btn.configure(text="Setting up...", state="disabled")
        self.api_status.update_status("connecting")
        
        def setup_thread():
            try:
                if GeminiECGDiagnosisClient:
                    self.diagnosis_client = GeminiECGDiagnosisClient(api_key, api_url)
                    self.root.after(0, self.on_api_setup_success)
                else:
                    self.root.after(0, self.on_api_setup_error, "Diagnosis module not available")
            except Exception as e:
                self.root.after(0, self.on_api_setup_error, str(e))
        
        threading.Thread(target=setup_thread, daemon=True).start()
    
    def on_api_setup_success(self):
        """Handle successful API setup"""
        self.setup_api_btn.configure(text="Setup API", state="normal")
        self.api_status.update_status("connected")
        self.diagnose_btn.configure(state="normal" if len(self.raw_ecg_values) > 100 else "disabled")
        self.show_success("API Setup", "Diagnosis API configured successfully!")
        
    def on_api_setup_error(self, error_msg: str):
        """Handle API setup error"""
        self.setup_api_btn.configure(text="Setup API", state="normal") 
        self.api_status.update_status("error")
        self.show_error("API Setup Error", f"Failed to setup API: {error_msg}")
    
    def start_diagnosis(self):
        """Start ECG diagnosis analysis"""
        if not self.diagnosis_client:
            self.show_warning("Diagnosis", "Please setup the API first.")
            return
        
        if len(self.raw_ecg_values) < 100:
            self.show_warning("Diagnosis", "Not enough ECG data for analysis. Please wait for more data.")
            return
        
        if self.diagnosis_worker and hasattr(self.diagnosis_worker, 'thread') and self.diagnosis_worker.thread.is_alive():
            self.show_info("Diagnosis", "Diagnosis already in progress.")
            return
        
        # Get patient information
        patient_info = self.get_patient_info()
        
        # Use last 2500 samples (10 seconds at 250Hz) for diagnosis
        ecg_data_for_diagnosis = self.raw_ecg_values[-2500:] if len(self.raw_ecg_values) >= 2500 else self.raw_ecg_values.copy()
        
        # Show progress
        self.progress_indicator.show_progress(0.1, "Starting diagnosis...")
        self.diagnose_btn.configure(state="disabled", text="Analyzing...")
        self.diagnosis_status_label.configure(text="Analyzing ECG data...", text_color=SECONDARY_BLUE)
        
        # Start diagnosis worker
        self.diagnosis_worker = DiagnosisWorker(
            self.diagnosis_client,
            ecg_data_for_diagnosis,
            patient_info,
            callback=self.on_diagnosis_completed,
            error_callback=self.on_diagnosis_error
        )
        self.diagnosis_worker.start()
        
        # Update progress periodically
        self.update_diagnosis_progress()
    
    def update_diagnosis_progress(self):
        """Update diagnosis progress indicator"""
        if self.diagnosis_worker and hasattr(self.diagnosis_worker, 'thread') and self.diagnosis_worker.thread.is_alive():
            # Simulate progress
            progress = min(0.9, time.time() % 30 / 30)  # Max 90% until complete
            self.progress_indicator.show_progress(progress, "Analyzing with AI...")
            self.root.after(500, self.update_diagnosis_progress)
    
    def on_diagnosis_completed(self, diagnosis: Dict[str, Any]):
        """Handle completed diagnosis"""
        self.progress_indicator.show_progress(1.0, "Diagnosis complete!")
        self.root.after(1000, self.progress_indicator.hide)
        
        self.last_diagnosis = diagnosis
        self.diagnosis_history.append({
            'timestamp': datetime.now().isoformat(),
            'diagnosis': diagnosis
        })
        
        # Update UI
        self.display_diagnosis(diagnosis)
        self.update_diagnosis_history()
        
        # Reset UI state
        self.diagnose_btn.configure(state="normal", text="Analyze ECG")
        self.diagnosis_status_label.configure(text="Diagnosis completed", text_color=SUCCESS_GREEN)
        
        # Update footer
        severity = diagnosis.get('severity', 'unknown')
        confidence = diagnosis.get('confidence', 0)
        self.update_footer_status(f"Diagnosis: {severity} severity ({confidence:.1%} confidence)")
    
    def on_diagnosis_error(self, error_message: str):
        """Handle diagnosis error"""
        self.progress_indicator.hide()
        self.diagnose_btn.configure(state="normal", text="Analyze ECG")
        self.diagnosis_status_label.configure(text=f"Diagnosis failed: {error_message}", text_color=ERROR_RED)
        
        # Show error in results
        error_text = f"Diagnosis Error ({datetime.now().strftime('%H:%M:%S')}):\n{error_message}\n\n"
        self.current_diagnosis_text.insert("1.0", error_text)
        
        self.show_error("Diagnosis Error", error_message)
    
    def get_patient_info(self) -> Optional[Dict[str, Any]]:
        """Get patient information from form inputs"""
        patient_info = {}
        
        age = self.age_entry.get().strip()
        if age:
            try:
                patient_info['age'] = int(age)
            except ValueError:
                pass
        
        gender = self.gender_combo.get()
        if gender:
            patient_info['gender'] = gender.lower()
        
        symptoms = self.symptoms_entry.get().strip()
        if symptoms:
            patient_info['symptoms'] = symptoms
        
        return patient_info if patient_info else None
    
    def toggle_auto_diagnosis(self):
        """Toggle automatic diagnosis mode"""
        self.auto_diagnosis_enabled = not self.auto_diagnosis_enabled
        
        if self.auto_diagnosis_enabled:
            self.auto_diagnosis_btn.configure(text="Auto: ON", style="success")
            self.diagnosis_status_label.configure(text="Auto-diagnosis enabled (every 30s)", text_color=SUCCESS_GREEN)
        else:
            self.auto_diagnosis_btn.configure(text="Auto: OFF", style="secondary") 
            self.diagnosis_status_label.configure(text="Auto-diagnosis disabled", text_color=TEXT_GRAY)
    
    def handle_serial_data(self, data: str):
        """Handle data received from serial port (called from worker thread)"""
        with self.data_lock:
            self.data_queue.append(data)
    
    def process_data_queue(self):
        """Process queued serial data in main thread"""
        if not self.serial_handler.is_connected:
            return
        
        with self.data_lock:
            data_to_process = self.data_queue.copy()
            self.data_queue.clear()
        
        for data in data_to_process:
            self.process_ecg_data(data)
        
        # Schedule next update
        if self.serial_handler.is_connected:
            self.root.after(50, self.process_data_queue)
    
    def process_ecg_data(self, data: str):
        """Process individual ECG data point"""
        try:
            # Parse ECG value (simplified - adapt based on your data format)
            ecg_value = None
            
            if data.startswith('DATA,'):
                parts = data.split(',')
                if len(parts) >= 3:
                    ecg_value = float(parts[2])
            else:
                # Try simple numeric format
                data_clean = data.strip()
                if data_clean and data_clean.replace('-', '').replace('.', '').isdigit():
                    ecg_value = float(data_clean)
            
            if ecg_value is not None:
                # Update statistics
                self.packets_received += 1
                
                # Add to plot
                self.ecg_plot.add_data_point(ecg_value)
                
                # Store for diagnosis
                self.raw_ecg_values.append(ecg_value)
                if len(self.raw_ecg_values) > self.diagnosis_buffer_size:
                    self.raw_ecg_values.pop(0)
                
                # Record if enabled
                if self.data_recorder and self.data_recorder.recording:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    self.data_recorder.write_data(timestamp, ecg_value)
                
                # Enable diagnosis button if enough data
                if len(self.raw_ecg_values) > 100 and self.diagnosis_client:
                    self.diagnose_btn.configure(state="normal")
                
        except Exception as e:
            print(f"Error processing ECG data: {e}")
    
    def check_auto_diagnosis(self):
        """Check if auto-diagnosis should be performed"""
        current_time = time.time()
        
        if (self.auto_diagnosis_enabled and 
            self.diagnosis_client and 
            len(self.raw_ecg_values) >= 1000 and
            current_time - self.last_auto_diagnosis >= self.auto_diagnosis_interval and
            not (self.diagnosis_worker and hasattr(self.diagnosis_worker, 'thread') and self.diagnosis_worker.thread.is_alive())):
            
            print("Performing automatic diagnosis...")
            self.last_auto_diagnosis = current_time
            self.start_diagnosis()
        
        # Schedule next check
        self.root.after(1000, self.check_auto_diagnosis)
    
    def update_statistics(self):
        """Update real-time statistics display"""
        if self.raw_ecg_values:
            # Calculate heart rate (simplified)
            if len(self.raw_ecg_values) > 500:  # At least 2 seconds of data
                try:
                    # Simple peak detection for heart rate
                    data = np.array(self.raw_ecg_values[-1250:])  # Last 5 seconds
                    peaks = []
                    threshold = np.mean(data) + 0.5 * np.std(data)
                    
                    for i in range(1, len(data) - 1):
                        if data[i] > data[i-1] and data[i] > data[i+1] and data[i] > threshold:
                            if not peaks or i - peaks[-1] >= 50:  # Minimum distance between peaks
                                peaks.append(i)
                    
                    if len(peaks) > 1:
                        intervals = np.diff(peaks) / 250.0  # Convert to seconds
                        avg_interval = np.mean(intervals)
                        heart_rate = 60.0 / avg_interval if avg_interval > 0 else 0
                        self.hr_label.configure(text=f"{heart_rate:.0f} BPM", text_color=SUCCESS_GREEN)
                    else:
                        self.hr_label.configure(text="-- BPM", text_color=TEXT_GRAY)
                        
                except Exception as e:
                    print(f"Error calculating heart rate: {e}")
                    self.hr_label.configure(text="-- BPM", text_color=TEXT_GRAY)
            
            # Update signal quality (simplified)
            if len(self.raw_ecg_values) > 100:
                recent_data = np.array(self.raw_ecg_values[-100:])
                noise_level = np.std(recent_data)
                
                if noise_level < 10:
                    quality = "Excellent"
                    color = SUCCESS_GREEN
                elif noise_level < 25:
                    quality = "Good"  
                    color = SUCCESS_GREEN
                elif noise_level < 50:
                    quality = "Fair"
                    color = WARNING_YELLOW
                else:
                    quality = "Poor"
                    color = ERROR_RED
                
                self.quality_label.configure(text=quality, text_color=color)
            
            # Update data count
            self.count_label.configure(text=f"{len(self.raw_ecg_values)}")
        
        # Update ECG statistics tab
        self.update_ecg_statistics_display()
        
        # Schedule next update
        self.root.after(1000, self.update_statistics)
    
    def display_diagnosis(self, diagnosis: Dict[str, Any]):
        """Display diagnosis results"""
        # Clear current results
        self.current_diagnosis_text.delete("1.0", "end")
        
        # Format diagnosis text
        diagnosis_text = self.format_diagnosis_text(diagnosis)
        self.current_diagnosis_text.insert("1.0", diagnosis_text)
        
        # Color code based on severity
        severity = diagnosis.get('severity', 'unknown').lower()
        if severity in SEVERITY_COLORS:
            color = SEVERITY_COLORS[severity]
            self.current_diagnosis_text.configure(text_color=color)
        
        # Switch to current results tab
        self.results_tabs.set("Current")
    
    def format_diagnosis_text(self, diagnosis: Dict[str, Any]) -> str:
        """Format diagnosis for display"""
        lines = []
        lines.append("=== ECG DIAGNOSIS REPORT ===")
        lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Primary diagnosis
        primary = diagnosis.get('primary_diagnosis', 'Unknown')
        severity = diagnosis.get('severity', 'unknown')
        confidence = diagnosis.get('confidence', 0.0)
        
        lines.append(f"PRIMARY DIAGNOSIS: {primary}")
        lines.append(f"SEVERITY: {severity.upper()}")
        lines.append(f"CONFIDENCE: {confidence:.1%}")
        lines.append("")
        
        # Secondary conditions
        secondary = diagnosis.get('secondary_conditions', [])
        if secondary:
            lines.append("POSSIBLE SECONDARY CONDITIONS:")
            for condition in secondary:
                lines.append(f"• {condition}")
            lines.append("")
        
        # Key findings
        findings = diagnosis.get('key_findings', [])
        if findings:
            lines.append("KEY ECG FINDINGS:")
            for finding in findings:
                lines.append(f"• {finding}")
            lines.append("")
        
        # Recommendations
        recommendations = diagnosis.get('recommendations', {})
        if recommendations:
            lines.append("RECOMMENDATIONS:")
            
            immediate = recommendations.get('immediate_actions', [])
            if immediate:
                lines.append("Immediate Actions:")
                for action in immediate:
                    lines.append(f"• {action}")
                lines.append("")
        
        return "\n".join(lines)
    
    def update_diagnosis_history(self):
        """Update diagnosis history display"""
        self.history_text.delete("1.0", "end")
        
        history_text = ""
        for i, entry in enumerate(reversed(self.diagnosis_history[-10:])):  # Last 10 diagnoses
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
        
        self.history_text.insert("1.0", history_text)
    
    def update_ecg_statistics_display(self):
        """Update ECG statistics display"""
        if not self.raw_ecg_values:
            return
        
        self.ecg_stats_text.delete("1.0", "end")
        
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
        stats_text += f"• RMS: {np.sqrt(np.mean(data**2)):.2f} μV\n"
        
        self.ecg_stats_text.insert("1.0", stats_text)
    
    def update_footer_status(self, status: str):
        """Update footer status text"""
        hr_text = self.hr_label.cget("text")
        last_diagnosis = "Never" if not self.diagnosis_history else "Recent"
        
        full_status = f"Status: {status} | Heart Rate: {hr_text} | Last Diagnosis: {last_diagnosis}"
        self.footer_status.configure(text=full_status)
    
    # Utility methods for dialogs
    def show_success(self, title: str, message: str):
        """Show success message dialog"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show warning message dialog"""
        messagebox.showwarning(title, message)
    
    def show_error(self, title: str, message: str):
        """Show error message dialog"""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show information message dialog"""
        messagebox.showinfo(title, message)
    
    def open_settings(self):
        """Open settings dialog"""
        self.show_info("Settings", "Settings dialog coming soon!")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🫀 ECG AI Heart Diagnosis - Help

Quick Start:
1. Enter your Gemini API key
2. Click 'Setup API'
3. Select serial port and click 'Connect'
4. Wait for ECG data, then click 'Analyze ECG'

Features:
• Real-time ECG monitoring
• AI-powered heart diagnosis
• Patient information integration
• Auto-diagnosis mode
• Data recording to CSV

For more help, see README.md
        """
        messagebox.showinfo("Help", help_text)
    def on_closing(self): 
        """Handle application closing"""
        if self.serial_handler and self.serial_handler.is_connected:
            self.serial_handler.disconnect()
        self.root.destroy()

def main():
    """Main entry point for modern ECG GUI"""
    try:
        app = ModernECGMainWindow()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start ECG AI application: {str(e)}")

if __name__ == "__main__":
    main()