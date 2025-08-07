# Windows Installation Guide for ECM_LLM

## 🪟 Windows Installation Instructions

This guide helps you install the ECG Monitor with AI diagnosis system on Windows.

### 🚨 Common Windows Issues & Solutions

#### Issue 1: Unicode Encoding Error
**Error**: `UnicodeDecodeError: 'gbk' codec can't decode byte`
**Solution**: This has been fixed in the latest version. If you still see this error:

```bash
# Option 1: Install from requirements.txt instead
pip install -r requirements.txt

# Option 2: Set environment variable
set PYTHONIOENCODING=utf-8
pip install -e .

# Option 3: Use PowerShell instead of Command Prompt
```

#### Issue 2: PyQt5 Installation Issues
**Error**: PyQt5 installation fails on Windows
**Solutions**:

```bash
# Option 1: Update pip first
python -m pip install --upgrade pip

# Option 2: Install PyQt5 separately
pip install PyQt5==5.15.7 PyQt5-tools==5.15.7.0

# Option 3: Use conda (if using Anaconda)
conda install pyqt

# Option 4: Install pre-compiled wheel
pip install --only-binary=all PyQt5
```

#### Issue 3: Serial Port Access Issues
**Error**: Cannot access COM ports
**Solutions**:
1. Install device drivers for your ESP32
2. Run command prompt as Administrator
3. Check Windows Device Manager for port conflicts
4. Ensure no other software is using the serial port

### ✅ Step-by-Step Installation

#### Step 1: Prepare Environment
```bash
# Check Python version (3.8+ required)
python --version

# Upgrade pip
python -m pip install --upgrade pip

# Optional: Create virtual environment
python -m venv ecg_env
ecg_env\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
# Method 1: Install from requirements file (recommended)
pip install -r requirements.txt

# Method 2: Manual installation
pip install pyserial>=3.5 numpy>=1.24.0 PyQt5>=5.15.0 pyqtgraph>=0.13.0 requests>=2.28.0 python-dotenv>=1.0.0

# Method 3: Package installation (if the above works)
pip install -e .
```

#### Step 3: Configure API
```bash
# Copy configuration template
copy .env.example .env

# Edit .env file with Notepad and add your API key:
# GEMINI_API_KEY=your_api_key_here
# GEMINI_API_URL=https://api.gptnb.ai/
```

#### Step 4: Test Installation
```bash
# Test without hardware
python test_diagnosis.py

# Run system check
python demo.py

# Launch application
python -m ecg_receiver.main
```

### 🔧 Windows-Specific Configuration

#### COM Port Detection
Windows COM ports usually appear as:
- `COM1`, `COM2`, `COM3`, etc.
- ESP32 typically shows as `COM3` to `COM20`
- Check Device Manager → Ports (COM & LPT)

#### Firewall Settings
If diagnosis fails, check Windows Firewall:
1. Allow Python through Windows Firewall
2. Allow outbound HTTPS connections
3. Check antivirus software blocking network access

#### Performance Optimization
```bash
# For better performance on Windows:
# 1. Close unnecessary applications
# 2. Run from SSD drive if available
# 3. Use dedicated USB ports (avoid hubs)
# 4. Disable Windows power management for USB ports
```

### 🐛 Troubleshooting Common Errors

#### Error: "No module named 'PyQt5'"
```bash
# Solution 1: Reinstall PyQt5
pip uninstall PyQt5 PyQt5-tools
pip install PyQt5==5.15.7

# Solution 2: Try different version
pip install PyQt5==5.15.4

# Solution 3: Use conda
conda install pyqt=5
```

#### Error: "Microsoft Visual C++ 14.0 is required"
```bash
# Download and install Microsoft Visual C++ Build Tools
# Or install Visual Studio Community (free)
# Alternative: Use pre-compiled wheels
pip install --only-binary=all PyQt5 pyqtgraph numpy
```

#### Error: "Access denied" during installation
```bash
# Run Command Prompt as Administrator
# Or use --user flag
pip install --user -r requirements.txt
```

#### Error: "SSL Certificate verify failed"
```bash
# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 📱 Windows Usage Tips

#### Running the Application
```bash
# Method 1: Command line
cd path\to\ecm_llm
python -m ecg_receiver.main

# Method 2: Create batch file (run_ecg.bat)
@echo off
cd /d "C:\path\to\ecm_llm"
python -m ecg_receiver.main
pause
```

#### Creating Desktop Shortcut
1. Right-click on Desktop → New → Shortcut
2. Target: `C:\path\to\python.exe -m ecg_receiver.main`
3. Start in: `C:\path\to\ecm_llm`
4. Name: "ECG AI Diagnosis"

### 💡 Performance Tips for Windows

#### Optimize for Real-time Processing
1. **Set High Priority**:
   - Open Task Manager
   - Find Python process
   - Right-click → Set Priority → High

2. **Disable Windows Updates** during critical monitoring

3. **Use Dedicated USB Port** (avoid USB hubs)

4. **Close Background Applications** that use CPU/memory

### 🆘 Getting Help

If you encounter issues not covered here:

1. **Check the main README.md** for general troubleshooting
2. **Run the demo script**: `python demo.py` for system validation
3. **Check Windows Event Viewer** for system errors
4. **Update Windows and drivers** to latest versions

### 📧 Contact Support

**Developer**: qiao@126.com  
**Repository**: https://github.com/GanQiao1990/ecm_llm  
**Issues**: Report Windows-specific issues on GitHub

---

*🪟 Windows Installation Guide - ECM_LLM v2.0*