"""
Data recording functionality for the ECG Receiver application.
"""

import os
import csv
from datetime import datetime

class DataRecorder:
    """Handles recording ECG data to CSV files."""
    
    def __init__(self, base_dir=None):
        """Initialize the data recorder.
        
        Args:
            base_dir (str, optional): Base directory for saving recordings.
                If None, a default directory will be created in the current directory.
        """
        self.recording = False
        self.csv_file = None
        self.csv_writer = None
        self.current_filename = None
        
        # Set up the data directory
        if base_dir is None:
            self.base_dir = os.path.join(os.path.expanduser('~'), 'ecg_recordings')
        else:
            self.base_dir = base_dir
            
        # Create the directory if it doesn't exist
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
    
    def start_recording(self):
        """Start recording data to a CSV file.
        
        Returns:
            bool: True if recording started successfully, False otherwise.
        """
        if self.recording:
            print("Already recording")
            return False
        
        # Generate a filename based on current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ecg_recording_{timestamp}.csv"
        self.current_filename = os.path.join(self.base_dir, filename)
        
        try:
            # Open the file for writing
            self.csv_file = open(self.current_filename, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            
            # Write header row
            self.csv_writer.writerow(['Timestamp', 'ECG (μV)'])
            
            self.recording = True
            print(f"Recording started. Data saved to: {self.current_filename}")
            return True
        except Exception as e:
            print(f"Error creating recording file: {e}")
            self.current_filename = None
            return False
    
    def stop_recording(self):
        """Stop recording data to CSV.
        
        Returns:
            str: The filename of the completed recording, or None if no recording was in progress.
        """
        if not self.recording:
            return None
        
        filename = self.current_filename
        
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None
        
        self.recording = False
        print("Recording stopped")
        
        return filename
    
    def write_data(self, timestamp, ecg_value):
        """Write a data point to the CSV file.
        
        Args:
            timestamp (str): Timestamp for the data point.
            ecg_value (float): ECG value in microvolts.
            
        Returns:
            bool: True if the data was written successfully, False otherwise.
        """
        if not self.recording or not self.csv_writer:
            return False
        
        try:
            self.csv_writer.writerow([timestamp, ecg_value])
            # Flush data to ensure it's written immediately
            if self.csv_file:
                self.csv_file.flush()
            return True
        except Exception as e:
            print(f"Error writing to CSV: {e}")
            return False
