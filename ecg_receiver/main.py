"""
Main entry point for the ECG Receiver application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from .gui.main_window import ECGMainWindow

def main():
    """Main function to start the ECG Receiver application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ECGMainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
