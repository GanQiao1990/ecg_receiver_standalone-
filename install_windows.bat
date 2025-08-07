@echo off
REM ECG AI Heart Diagnosis - Windows Installation Script
title ECG AI Heart Diagnosis Setup

echo ======================================
echo 🫀 ECG AI Heart Diagnosis - Windows Setup
echo ======================================
echo.

REM Check Python installation
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo ✅ Please install Python 3.8+ from: https://www.python.org/downloads/
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python found
)

REM Check pip
echo.
echo 📦 Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    echo Installing pip...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
) else (
    echo ✅ pip is available
)

REM Upgrade pip
echo.
echo ⬆️  Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo.
echo ⬇️  Installing ECG AI dependencies...
echo This may take several minutes, please wait...
echo.

echo 📋 Installing core dependencies...
python -m pip install pyserial^>=3.5 numpy^>=1.24.0 requests^>=2.28.0 python-dotenv^>=1.0.0

echo.
echo 🎨 Installing modern GUI dependencies...
python -m pip install customtkinter^>=5.2.0 matplotlib^>=3.7.0 Pillow^>=10.0.0 psutil^>=5.9.0

echo.
echo 📱 Installing optional legacy GUI dependencies...
python -m pip install PyQt5^>=5.15.0 pyqtgraph^>=0.13.0 2>nul || (
    echo ⚠️  Legacy GUI dependencies failed - optional, continuing...
)

REM Test installation
echo.
echo 🧪 Testing installation...
python -c "import customtkinter, matplotlib, numpy, serial, requests; print('✅ All core modules imported successfully')" || (
    echo ❌ Installation verification failed
    pause
    exit /b 1
)

REM Create desktop shortcuts
echo.
echo 🔗 Creating desktop shortcuts...
set DESKTOP=%USERPROFILE%\Desktop
set CURRENT_DIR=%~dp0

REM Modern GUI shortcut
echo @echo off > "%DESKTOP%\ECG Modern GUI.bat"
echo cd /d "%CURRENT_DIR%" >> "%DESKTOP%\ECG Modern GUI.bat"
echo python launch_modern_gui.py >> "%DESKTOP%\ECG Modern GUI.bat"
echo pause >> "%DESKTOP%\ECG Modern GUI.bat"

REM Legacy GUI shortcut
echo @echo off > "%DESKTOP%\ECG Legacy GUI.bat"
echo cd /d "%CURRENT_DIR%" >> "%DESKTOP%\ECG Legacy GUI.bat"  
echo python -m ecg_receiver.main >> "%DESKTOP%\ECG Legacy GUI.bat"
echo pause >> "%DESKTOP%\ECG Legacy GUI.bat"

echo ✅ Desktop shortcuts created

REM Installation complete
echo.
echo ====================================
echo 🎉 Installation Complete!
echo ====================================
echo.
echo 🚀 To launch ECG AI Heart Diagnosis:
echo    Option 1: Double-click "ECG Modern GUI" on Desktop
echo    Option 2: Double-click "ECG Legacy GUI" on Desktop  
echo    Option 3: Run "python launch_modern_gui.py" in this folder
echo.
echo ⚙️  Next steps:
echo    1. Connect your ESP32 + ADS1292R ECG hardware via USB
echo    2. Launch the application
echo    3. Set up your Gemini 2.5 Flash API key
echo    4. Select the correct COM port
echo    5. Start ECG monitoring with AI diagnosis
echo.
echo 📚 Documentation:
echo    • README.md - Complete setup guide
echo    • PERFORMANCE_OPTIMIZATION_REPORT.md - Technical details
echo.
echo ❤️  Ready for ECG AI Heart Diagnosis!
echo.
pause