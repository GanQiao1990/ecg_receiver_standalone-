# 🚀 Installation Guide - ECG AI Heart Diagnosis

Complete installation guide for setting up the ECG AI Heart Diagnosis system with modern GUI and performance optimizations.

---

## 📋 **Quick Installation Options**

### **Option 1: Automated Installation (Recommended)**

#### **Windows Users:**
1. Download `install_windows.bat`
2. Right-click → "Run as Administrator"
3. Follow the prompts
4. Launch via desktop shortcuts

#### **Linux/macOS Users:**
```bash
# Download and run the quick install script
chmod +x quick_install.sh
./quick_install.sh
```

#### **All Platforms (Python):**
```bash
# Enhanced installation with system checking
python setup_enhanced.py
```

### **Option 2: Manual Installation**

#### **Prerequisites:**
- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **pip** (usually included with Python)
- **Git** (optional, for cloning repository)

#### **Step-by-step Installation:**

1. **Clone or Download the Repository:**
```bash
git clone https://github.com/GanQiao1990/ecg_receiver_standalone-.git
cd ecg_receiver_standalone-
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Launch the Application:**
```bash
# Kivy GUI (recommended)
python launch_kivy_gui.py

# Legacy GUI (fallback)
python -m ecg_receiver.main
```

---

## 📦 **Dependencies Explained**

### **Core ECG Processing:**
```text
pyserial>=3.5           # ESP32 communication
numpy>=1.24.0           # Signal processing
requests>=2.28.0        # AI API communication
python-dotenv>=1.0.0    # Configuration management
```

### **Kivy GUI Framework:**
```text
kivy>=2.3.0            # Cross-platform GUI framework
psutil>=5.9.0          # Performance monitoring
```

### **Legacy GUI (Optional):**
```text
PyQt5>=5.15.0          # Traditional GUI framework
pyqtgraph>=0.13.0      # Legacy plotting
```

### **Development & Testing (Optional):**
```text
pytest>=7.0.0          # Testing framework
pytest-qt>=4.2.0       # GUI testing utilities
```

---

## 🖥️ **Platform-Specific Instructions**

### **Windows 10/11**

#### **Method 1: One-Click Install**
1. Download `install_windows.bat`
2. Right-click → "Run as Administrator"
3. Wait for installation to complete
4. Use desktop shortcuts to launch

#### **Method 2: Manual PowerShell**
```powershell
# Check Python
python --version

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Launch Kivy GUI
python launch_kivy_gui.py
```

#### **Windows Troubleshooting:**
- **Python not found**: Install from [python.org](https://www.python.org) and check "Add to PATH"
- **SSL Certificate errors**: Run `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt`
- **Permission errors**: Run Command Prompt as Administrator

### **Linux (Ubuntu/Debian)**

#### **Method 1: Quick Script**
```bash
# Download and run
wget -O quick_install.sh https://raw.githubusercontent.com/GanQiao1990/ecg_receiver_standalone-/main/quick_install.sh
chmod +x quick_install.sh
./quick_install.sh
```

#### **Method 2: Manual Installation**
```bash
# Update system
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install system dependencies
sudo apt install python3-dev build-essential

# Install Python packages
pip3 install -r requirements.txt

# Launch application
python3 launch_kivy_gui.py
```

#### **Linux ARM (Raspberry Pi/Development Boards)**
```bash
# Use the dedicated ARM installation script
chmod +x install_arm_linux.sh
./install_arm_linux.sh

# For Raspberry Pi optimization
chmod +x optimize_raspberry_pi.sh
./optimize_raspberry_pi.sh
```

### **macOS**

#### **Prerequisites:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

#### **Installation:**
```bash
# Clone repository
git clone https://github.com/GanQiao1990/ecg_receiver_standalone-.git
cd ecg_receiver_standalone-

# Install dependencies
pip3 install -r requirements.txt

# Launch application
python3 launch_kivy_gui.py
```

---

## 🔧 **Hardware Setup**

### **Required Hardware:**
- **ESP32 Development Board** (NodeMCU, DevKit, etc.)
- **ADS1292R ECG Front-end** (Texas Instruments)
- **ECG Electrodes** (3-lead or 5-lead configuration)
- **USB Cable** (ESP32 to Computer)

### **Connection Setup:**
1. Connect ADS1292R to ESP32 via SPI
2. Connect ECG electrodes to ADS1292R analog inputs
3. Flash ECG firmware to ESP32
4. Connect ESP32 to computer via USB
5. Note the serial port (COM3, /dev/ttyUSB0, etc.)

### **Firmware Configuration:**
- **Baud Rate**: 115200
- **Data Format**: CSV or raw ADC values
- **Sampling Rate**: 250 Hz (recommended)
- **Data Frame**: Timestamp,Channel1,Channel2

---

## ⚙️ **Configuration Setup**

### **1. API Configuration:**
1. Get Gemini 2.5 Flash API key from [https://api.gptnb.ai/](https://api.gptnb.ai/)
2. Open the application
3. Click "Setup API" in the diagnosis panel
4. Enter your API key and save

### **2. Serial Port Configuration:**
1. Connect your ESP32 hardware
2. Launch the application
3. Click "Scan Ports" to detect available ports
4. Select your ESP32 port from dropdown
5. Click "Connect" to start monitoring

### **3. Optional: Environment File:**
Create `.env` file in project root:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_BASE_URL=https://api.gptnb.ai/

# Serial Configuration (optional defaults)
DEFAULT_SERIAL_PORT=COM3
DEFAULT_BAUD_RATE=115200

# GUI Configuration
DEFAULT_GUI_THEME=dark
ENABLE_PERFORMANCE_MONITORING=true
```

---

## 🧪 **Testing Installation**

### **Quick Test:**
```bash
# Run the validation script
python validate_performance.py

# Expected output:
# ✅ All performance optimizations validated successfully!
# 🚀 GUI is ready for high-performance ECG processing
```

### **Manual Component Testing:**
```bash
# Test Kivy GUI import
python -c "import kivy; print('✅ Kivy GUI: OK')"

# Test performance optimizations  
python -c "from ecg_receiver.core.circular_buffer import CircularECGBuffer; print('✅ Circular Buffer: OK')"

# Test AI diagnosis (requires API key)
python test_diagnosis.py
```

### **GUI Launch Test:**
```bash
# Test Kivy interface
python launch_kivy_gui.py

# Test legacy interface (fallback)
python -m ecg_receiver.main
```

---

## 🎯 **Performance Optimization**

### **Automatic Optimizations (Included):**
- **Memory Management**: Circular buffer prevents memory leaks
- **GUI Rendering**: Efficient Kivy canvas drawing (~30 FPS via Clock scheduling)
- **Data Processing**: Background threading prevents UI blocking
- **Performance Monitoring**: Real-time CPU/Memory tracking

### **Manual Performance Tuning:**

#### **For High-Speed ECG (500+ Hz):**
```python
# Edit ecg_receiver/core/circular_buffer.py
# Increase buffer size
BUFFER_SIZE = 10000  # 40 seconds at 250Hz
```

#### **For Low-End Hardware:**
```python
# Edit ecg_receiver/gui_kivy/main_app.py
# Reduce update frequency by lowering FPS
# Find: Clock.schedule_interval(self.update_plot, 1 / 30.0)
# Change to e.g. 20 FPS to reduce CPU usage:
# Clock.schedule_interval(self.update_plot, 1 / 20.0)
```

#### **Memory Optimization:**
```python
# Edit main GUI settings in ecg_receiver/gui_kivy/main_app.py
# Reduce time window or max_points for lower memory/CPU
self.time_window_sec = 8       # e.g., from 10 to 8 seconds
self.plot.max_points = 1500    # e.g., from 2000 to 1500
```

---

## 🚨 **Troubleshooting**

### **Common Installation Issues:**

#### **1. "Module not found" errors:**
```bash
# Reinstall with specific Python version
python3.9 -m pip install -r requirements.txt
python3.9 launch_kivy_gui.py
```

#### **2. GUI not launching:**
```bash
# Check display forwarding (Linux/SSH)
export DISPLAY=:0.0

# Kivy dependencies (if missing)
conda install -c conda-forge kivy numpy pyserial  # Recommended
```

#### **3. Serial port access denied:**
```bash
# Linux: Add user to dialout group
sudo usermod -a -G dialout $USER
# Logout and login again

# Windows: Check Device Manager for COM port conflicts
```

#### **4. Performance issues:**
```bash
# Run performance test
python test_gui_performance.py

# Check system resources
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}% RAM: {psutil.virtual_memory().percent}%')"
```

#### **5. AI Diagnosis not working:**
- Check API key configuration
- Verify internet connection
- Test with `python test_diagnosis.py`
- Check API endpoint: [https://api.gptnb.ai/](https://api.gptnb.ai/)

### **Performance Monitoring:**
The application includes real-time performance monitoring (via `psutil`). Watch for:
- **CPU Usage**: Typically < 10% during normal operation
- **Memory**: Typically < 100MB for standard sessions
- **FPS**: Aim > 20 for smooth plotting
- **Buffer**: ECG data buffer utilization

---

## 📚 **Additional Documentation**

- **[PERFORMANCE_OPTIMIZATION_REPORT.md](PERFORMANCE_OPTIMIZATION_REPORT.md)**: Detailed performance improvements
- **[README.md](README.md)**: Main project documentation

---

## 🎉 **Installation Complete!**

### **Next Steps:**
1. **🔌 Connect Hardware**: ESP32 + ADS1292R ECG system
2. **🚀 Launch App**: Use desktop shortcuts or `python launch_kivy_gui.py`
3. **⚙️ Configure API**: Set up Gemini 2.5 Flash API key
4. **📊 Start Monitoring**: Select serial port and begin ECG analysis
5. **🤖 AI Diagnosis**: Enable automatic heart condition analysis

### **Support:**
- **Issues**: Report at [GitHub Issues](https://github.com/GanQiao1990/ecg_receiver_standalone-/issues)
- **Documentation**: Check project README and guides
- **Performance**: Use built-in monitoring and validation tools

**❤️ Ready for ECG AI Heart Diagnosis!** 🫀✨