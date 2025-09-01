# ECG Receiver with AI Heart Diagnosis

A comprehensive standalone application for real-time ECG data visualization and AI-powered heart problem diagnosis using Gemini 2.5 Flash model. This system combines real-time ECG monitoring from ADS1292R sensor connected to an ESP32 board with advanced AI analysis for heart condition detection.

<img width="1385" height="936" alt="4c9a318bef7ddaf9603107596a4fd978" src="https://github.com/user-attachments/assets/d1360387-bec2-4f51-8e00-6c41ae5e2565" />


## 🔥 New Features v2.0

- **🤖 AI-Powered Heart Diagnosis**: Real-time heart condition analysis using Gemini 2.5 Flash model
- **📊 Comprehensive ECG Analysis**: Automated detection of arrhythmias, heart rate abnormalities, and other cardiac conditions
- **👥 Patient Information Integration**: Include patient demographics and symptoms for more accurate diagnosis
- **📈 Real-time Statistics**: Live ECG statistics including heart rate estimation, voltage analysis, and signal quality
- **🔄 Auto-Diagnosis Mode**: Automatic periodic analysis of incoming ECG data
- **📋 Diagnosis History**: Track and review previous diagnoses with timestamps
- **⚠️ Severity Assessment**: Color-coded severity levels (Low, Moderate, High, Critical)
- **💡 Clinical Recommendations**: AI-generated recommendations for immediate actions, follow-up, and lifestyle changes

## ⚡ Quickstart (Kivy GUI – Recommended)

Kivy is the default recommended GUI for an easier cross-platform setup and smoother debugging.

1. Create and activate a Python environment
   - Conda/Mamba (recommended):
     ```bash
     conda create -n ecg python=3.11 -y
     conda activate ecg
     ```
   - venv (alternative):
     ```bash
     python -m venv .venv && source .venv/bin/activate
     ```

2. Install dependencies
   - Best for Linux/macOS: use conda-forge to install Kivy (bundles SDL2 deps):
     ```bash
     conda install -c conda-forge kivy numpy pyserial -y
     pip install -r requirements.txt
     ```
   - Pip-only (works on Windows; on Linux you may need SDL2 system libs). China mainland mirror example:
     ```bash
     pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
     ```

3. Run the Kivy GUI
   ```bash
   python launch_kivy_gui.py
   ```

4. Connect your device
   - Select the serial port and click Connect.
   - Optional: Start Recording to save CSV.

Notes (Linux): if you cannot open the serial port: `sudo usermod -a -G dialout $USER` then log out/in.

## Features

### Core ECG Monitoring
- **Real-time ECG Monitoring**: View live ECG waveform with a scrolling display
- **Enhanced User Interface**: Modern GUI with diagnosis panel and tabbed results view
- **Data Logging**: Save ECG data to timestamped CSV files for later analysis
- **Cross-platform**: Works on Windows, macOS, and Linux

### AI Diagnosis Capabilities
- **Heart Rate Analysis**: Automatic detection of tachycardia, bradycardia, and rate variations
- **Rhythm Assessment**: Detection of irregular rhythms, arrhythmias, and conduction abnormalities  
- **Morphology Analysis**: QRS complex analysis and waveform pattern recognition
- **Risk Factor Identification**: Assessment of cardiac risk factors based on ECG patterns
- **Confidence Scoring**: AI confidence levels for each diagnosis
- **Clinical Context**: Integration of patient symptoms and demographics for enhanced accuracy

## Project Structure

```
ecg_receiver_standalone-/
├── 🚀 Installation Files
│   ├── install_windows.bat         # Windows one-click installer
│   ├── quick_install.sh            # Linux/macOS quick installer
│   ├── setup_enhanced.py           # Python cross-platform installer
│   └── validate_installation.py    # Installation verification tool
│
├── 📖 Documentation
│   ├── README.md                   # Main project documentation
│   ├── INSTALLATION.md             # Comprehensive installation guide
│   ├── PERFORMANCE_OPTIMIZATION_REPORT.md  # Performance improvements
│   └── TKINTER_DESIGNER_GUIDE.md   # GUI customization guide
│
├── 🫀 ECG Core System
│   ├── ecg_receiver/               # Core ECG monitoring modules
│   │   ├── core/                   # Core functionality
│   │   │   ├── circular_buffer.py  # 🆕 Memory-efficient data storage
│   │   │   ├── performance_monitor.py # 🆕 Real-time performance tracking
│   │   │   ├── data_recorder.py    # CSV data logging
│   │   │   └── serial_handler.py   # ESP32 communication
│   │   ├── gui/                    # Legacy PyQt5 interface
│   │   │   └── main_window.py      # Legacy GUI with AI diagnosis
│   │   ├── gui_kivy/                # 🆕 Kivy interface (recommended)
│   │   │   └── main_app.py          # Kivy app entry
│   │   └── main.py                 # Legacy application entry point
│   ├── ecg_diagnosis.py            # AI diagnosis engine (Gemini 2.5 Flash)
│   └── launch_kivy_gui.py          # 🆕 Kivy GUI launcher
│
├── 🧪 Testing & Validation
│   ├── test_diagnosis.py           # AI diagnosis functionality tests
│   ├── test_gui_performance.py     # 🆕 GUI performance analysis
│   └── validate_performance.py     # 🆕 Performance optimization validator
│
├── ⚙️ Configuration
│   ├── requirements.txt            # Updated Python dependencies
│   ├── .env.example               # Environment configuration template
│   └── setup.py                   # Package installation script
│
└── 🔧 Hardware Support Files
    ├── install_arm_linux.sh       # ARM Linux installation (Raspberry Pi)
    └── optimize_raspberry_pi.sh   # Raspberry Pi performance tuning
└── setup.py                  # Package installation configuration
```

## Requirements

### Hardware
- ESP32 with ADS1292R shield
- USB cable for connecting ESP32 to computer

### ESP32-ADS1292R ECG Monitoring System Architecture Diagram
<img width="454" height="669" alt="Image" src="https://github.com/user-attachments/assets/3d694262-bd15-4292-82c5-45b39c9143ca" />

<img width="349" height="656" alt="Image" src="https://github.com/user-attachments/assets/45de92ee-87d6-4add-b2f8-eb667b3115ec" />

<img width="718" height="277" alt="Image" src="https://github.com/user-attachments/assets/eb52e943-01b0-4b9c-aa5b-f4efd12c7115" />

### Software
- Python 3.8 or higher
- Kivy (recommended GUI)
- PyQt5 and PyQtGraph (legacy PyQt GUI, optional)
- pyserial for serial communication
- numpy for data processing
- requests for API communication
- python-dotenv for configuration management

### AI Diagnosis
- Gemini 2.5 Flash API key (from https://deepresearch2agi.cn/)
- Internet connection for AI analysis

## Installation

> **📖 Complete Installation Guide**: See **[INSTALLATION.md](INSTALLATION.md)** for detailed platform-specific instructions, troubleshooting, and advanced setup options.

### 🚀 **Quick Install Options**

#### **Option 1: Automated Installation (Recommended)**

**Windows:**
- Download `install_windows.bat` → Right-click → "Run as Administrator"

**Linux/macOS:**
```bash
chmod +x quick_install.sh && ./quick_install.sh
```

**All Platforms:**
```bash
python setup_enhanced.py
```

#### **Option 2: Manual Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/GanQiao1990/ecg_receiver_standalone-.git
   cd ecg_receiver_standalone-
   ```

2. **Install dependencies**
   - Option A (recommended on Linux/macOS): conda-forge for Kivy, pip for the rest
     ```bash
     conda create -n ecg python=3.11 -y
     conda activate ecg
     conda install -c conda-forge kivy numpy pyserial -y
     pip install -r requirements.txt
     ```
   - Option B (pip-only): include a mirror if needed (China mainland example)
     ```bash
     pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
     ```

3. **Launch the GUI**
   - Kivy (recommended):
     ```bash
     python launch_kivy_gui.py
     ```
   - PyQt5 (legacy):
     ```bash
     python -m ecg_receiver.main
     ```

### **New in v2.0: Performance Optimizations**
- ⚡ **60-80% memory usage reduction** with circular buffer system
- 🚀 **40-60% faster plotting** with matplotlib blitting optimization
- 📊 **Real-time performance monitoring** built into the GUI
- 🧠 **Background AI processing** prevents interface blocking
- 💾 **Memory leak prevention** with automatic cleanup

### Method 3: Legacy Installation (Original)
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials**
   ```bash
   cp .env.example .env
   # Edit .env file and add your Gemini API key
   ```

### Method 2: Package Installation

1. **Install with pip**
   ```bash
   pip install -e .
   ```

## Configuration

### API Setup

1. **Get Gemini API Key**
   - Sign up at https://deepresearch2agi.cn/
   - Obtain your API key for Gemini 2.5 Flash model

2. **Configure Environment**
   ```bash
   # Create .env file
   GEMINI_API_KEY=your_api_key_here
   GEMINI_API_URL=https://deepresearch2agi.cn/
   ```

3. **Test API Connection**
   ```bash
   python test_diagnosis.py
   ```

## Usage

### Quick Start

1. **Launch the application**
   - Kivy (recommended):
     ```bash
     python launch_kivy_gui.py
     ```
   - PyQt (legacy):
     ```bash
     python -m ecg_receiver.main
     ```

2. **Setup AI Diagnosis** (in the application)
   - Enter your Gemini API key in the "AI Diagnosis Configuration" panel
   - Click "Setup API" to initialize the diagnosis system
   - Status should show "Configured ✓"

3. **Connect to ECG Device**
   - Select your ESP32's COM port from the dropdown
   - Click "Connect" to begin receiving data
   - ECG waveform should appear in real-time

4. **Perform Heart Diagnosis**
   - Wait for sufficient ECG data (at least 4 seconds)
   - Optionally enter patient information (age, gender, symptoms)
   - Click "Analyze Current ECG" for on-demand diagnosis
   - Or enable "Auto-Diagnosis" for continuous analysis every 30 seconds

### Using the Diagnosis Features

#### Manual Diagnosis
- **Current ECG Analysis**: Click "Analyze Current ECG" to get immediate diagnosis
- **Patient Information**: Fill in age, gender, and symptoms for more accurate results
- **View Results**: Check the "Current Diagnosis" tab for detailed analysis

#### Auto-Diagnosis Mode
- **Enable**: Click "Enable Auto-Diagnosis" to analyze ECG every 30 seconds
- **Monitor**: Watch for automatic updates in the diagnosis panel
- **History**: Review all diagnoses in the "History" tab

#### Understanding Results
- **Primary Diagnosis**: Main heart condition identified
- **Severity Levels**: 
  - 🟢 **Low**: Minor abnormalities, routine monitoring
  - 🟡 **Moderate**: Attention needed, consider follow-up
  - 🟠 **High**: Significant concern, medical consultation recommended
  - 🔴 **Critical**: Immediate medical attention required
- **Confidence**: AI confidence level (0-100%)
- **Recommendations**: Suggested immediate actions, follow-up, and lifestyle changes

### Advanced Features

#### ECG Statistics
- **Real-time Metrics**: Heart rate, voltage statistics, signal quality
- **Peak Detection**: Automatic QRS complex identification
- **Heart Rate Variability**: RR interval analysis
- **Data Quality**: Sample count, duration, signal-to-noise ratio

#### Data Management
- **Recording**: Save ECG data to timestamped CSV files (default folder: `~/ecg_recordings`)
- **History**: Access previous diagnoses with timestamps
- **Export**: Diagnosis results can be copied from the text panels

## ESP32 Configuration

1. **Prepare ESP32 Firmware**
   - Ensure your firmware prints ECG samples over Serial at 57600 baud.
   - Supported formats:
     - CSV: `DATA,timestamp,ecg_value,resp_value,heart_rate,status`
     - Simple numeric: a single value per line (e.g., `-7`, `1024`)
   - You can adapt common ADS1292R + ESP32 examples from Arduino/ESP-IDF projects to match one of the formats above.

2. **Hardware Connection**
   - Connect ESP32 to your computer via USB
   - Wire the ADS1292R to the ESP32 according to your chosen firmware's pin mapping

## Using the Application

1. **Launch the application** as described above
2. **Select your ESP32's COM port** from the dropdown menu
3. **Click "Connect"** to begin receiving data
4. **Click "Start Recording"** to save data to a CSV file (optional)
5. **Monitor the ECG waveform** in the main display

## Troubleshooting

### Connection Issues

- **No COM ports available**:
  - Make sure the ESP32 is properly connected
  - Install the correct USB drivers for your ESP32
  - Try unplugging and reconnecting the USB cable
  - On Linux, you may need permissions to access serial ports: `sudo usermod -a -G dialout $USER` (then logout/login)

- **Connection fails**:
  - Check that the baud rate matches (default: 57600)
  - Ensure no other program is using the serial port
  - Try different timeout values (the improved version automatically tries multiple timeouts)
  - Verify the ESP32 is sending data in the expected format

- **No data received**:
  - Check the ESP32 serial monitor to verify it's sending data
  - Ensure the data format matches: `DATA,timestamp,ecg_value,resp_value,heart_rate,status`
  - Try different serial port settings (the improved version tries multiple configurations)
  - Check for loose connections or cable issues

- **Data parsing errors**:
  - Verify the ESP32 is sending properly formatted CSV data
  - Check for missing commas or extra characters in the data stream
  - Enable debug logging to see raw data being received

### Testing Connection

Use the included test script to debug connection issues:

```bash
python test_connection.py
```

### AI Diagnosis Testing

Test the diagnosis system without hardware:

```bash
python test_diagnosis.py
```

This will run sample ECG patterns through the AI diagnosis system and show results.

## Troubleshooting

### Connection Issues

- **No COM ports available**:
  - Make sure the ESP32 is properly connected
  - Install the correct USB drivers for your ESP32
  - Try unplugging and reconnecting the USB cable
  - On Linux, you may need permissions to access serial ports: `sudo usermod -a -G dialout $USER` (then logout/login)

- **Connection fails**:
  - Check that the baud rate matches (default: 57600)
  - Ensure no other program is using the serial port
  - Try different timeout values (the improved version automatically tries multiple timeouts)
  - Verify the ESP32 is sending data in the expected format

### AI Diagnosis Issues

- **"API Setup Failed"**:
  - Verify your API key is correct and active
  - Check internet connection
  - Ensure API URL is correct: https://deepresearch2agi.cn/
  - Try testing with: `python test_diagnosis.py`

- **"Not enough ECG data for analysis"**:
  - Wait for at least 4 seconds of ECG data
  - Check that ECG device is connected and sending data
  - Verify data is being received (check ECG statistics tab)

- **Diagnosis takes too long or fails**:
  - Check internet connection stability
  - Verify API rate limits haven't been exceeded
  - Try again after a few minutes
  - Check diagnosis error messages in the results panel

- **Poor diagnosis quality**:
  - Ensure good ECG signal quality (minimal noise)
  - Provide patient information for better context
  - Use longer ECG segments (10+ seconds recommended)
  - Check that electrodes are properly connected

### Performance Issues

- **Slow or choppy display**:
  - The buffer size has been increased to 2000 points (8 seconds of data)
  - Try reducing the plot update rate if your system is slow
  - Close other applications that might be using system resources
  - Disable auto-diagnosis if system is slow

- **High CPU usage**:
  - The improved version uses more efficient data handling
  - Consider reducing the sample rate on the ESP32 side if needed
  - Disable auto-diagnosis mode if not needed
  - Close unused tabs in the diagnosis panel

### Data Format Issues

- **"Invalid data format" errors**:
  - This has been fixed in v2.0! The system now automatically detects simple numeric data format
  - Supported formats: single values per line (like -7, -6, -5) or CSV format
  - Use `python analyze_data_format.py` to check your data format

### API Configuration

- **Environment Variables**: Create a `.env` file with your API configuration:
  ```bash
  GEMINI_API_KEY=your_api_key_here
  GEMINI_API_URL=https://deepresearch2agi.cn/
  ```

- **API Key Management**: 
  - Never commit API keys to version control
  - Use environment variables or the GUI configuration
  - Keep your API key secure and don't share it

### Performance Issues

- **Slow or choppy display**:
  - The buffer size has been increased to 2000 points (8 seconds of data)
  - Try reducing the plot update rate if your system is slow
  - Close other applications that might be using system resources

- **High CPU usage**:
  - The improved version uses more efficient data handling
  - Consider reducing the sample rate on the ESP32 side if needed

### Debug Mode

To enable detailed logging, modify the source code to increase verbosity or add print statements to track data flow.

## Improvements in This Version

- **Enhanced connection handling**: Multiple timeout attempts and better error recovery
- **Thread-safe data processing**: Uses Qt signals for safe GUI updates
- **Better error messages**: More descriptive error dialogs and status updates
- **Improved data validation**: Validates data format before processing
- **Larger data buffer**: 8 seconds of data display instead of 5
- **Connection testing**: Included test script for debugging
- **Automatic reconnection attempts**: Basic framework for reconnection (can be extended)
- **Better resource management**: Proper cleanup of threads and file handles

## Data Format

The ECG receiver now supports multiple data formats:

### Standard Format (Recommended)
```
DATA,timestamp,ecg_value,resp_value,heart_rate,status
```
Example: `DATA,1234567890,1024,512,75,OK`

### Simple Numeric Format (Auto-detected)
If your ESP32 sends simple numeric values (like in your case), the receiver will automatically detect and process them:
```
-7
-6
-5
1024
1050
```

### Multiple Values Per Line
Space or comma separated values:
```
1024 512 75
1050,520,76
```

## Fixing "Invalid data format" Errors

If you see "Invalid data format" errors like:
```
Invalid data format: -7...
Invalid data format: -6...
```

**This has been fixed!** The improved version now:
1. ✓ Automatically detects simple numeric data format
2. ✓ Processes single values per line (like -7, -6, -5)
3. ✓ Handles both positive and negative values
4. ✓ Works with integer and decimal values

### Testing Your Data Format

Use the data format analyzer to see what your ESP32 is sending:
```bash
python analyze_data_format.py
```

This will:
- Connect to your ESP32 (COM7 or first available port)
- Show you exactly what data format is being sent
- Analyze the data rate and format
- Provide specific recommendations

## License

This project is open source and available under the MIT License.

## Acknowledgments

- This project utilizes the ADS1292R ECG front-end chip for high-quality ECG signal acquisition
- Built with PyQt5 and PyQtGraph for efficient real-time visualization
