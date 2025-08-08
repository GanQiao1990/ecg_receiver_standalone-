#!/bin/bash
# ECG AI Heart Diagnosis - Quick Installation Script
# Supports Linux, macOS, and Windows (WSL/Git Bash)

set -e

echo "🫀 ECG AI Heart Diagnosis - Quick Setup"
echo "========================================"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

echo "📱 Detected OS: $OS"

# Check Python
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 found"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python found"
else
    echo "❌ Python not found. Please install Python 3.8+."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "📋 Python version: $PYTHON_VERSION"

# Check pip
echo "📦 Checking pip..."
if $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "✅ pip is available"
else
    echo "❌ pip not found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PYTHON_CMD get-pip.py
    rm get-pip.py
fi

# Install dependencies
echo "⬇️  Installing dependencies..."
echo "This may take a few minutes..."

# Core dependencies
echo "📋 Installing core dependencies..."
$PYTHON_CMD -m pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Kivy GUI dependencies
echo "🎨 Installing Kivy GUI dependencies..."
$PYTHON_CMD -m pip install kivy>=2.3.0 psutil>=5.9.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Core ECG dependencies  
echo "🔬 Installing ECG processing dependencies..."
$PYTHON_CMD -m pip install pyserial>=3.5 numpy>=1.24.0 requests>=2.28.0 python-dotenv>=1.0.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Optional legacy GUI (install without failing)
echo "📱 Installing optional legacy GUI..."
$PYTHON_CMD -m pip install PyQt5>=5.15.0 pyqtgraph>=0.13.0 || echo "⚠️  Legacy GUI dependencies optional (continuing)"

echo ""
echo "🧪 Testing installation..."

# Quick test
$PYTHON_CMD -c "
import kivy, numpy, serial, requests, psutil
print('✅ All core modules imported successfully')
" || {
    echo "❌ Installation verification failed"
    exit 1
}

echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
echo "🚀 To launch the Kivy ECG GUI:"
echo "   $PYTHON_CMD launch_kivy_gui.py"
echo ""
echo "📋 To launch the legacy GUI:"
echo "   $PYTHON_CMD -m ecg_receiver.main"
echo ""
echo "⚙️  Next steps:"
echo "   1. Set up your Gemini 2.5 Flash API key in the GUI"
echo "   2. Connect your ESP32 + ADS1292R ECG hardware"
echo "   3. Select the correct serial port"
echo "   4. Start real-time ECG monitoring with AI diagnosis"
echo ""
echo "❤️  Ready for ECG AI Heart Diagnosis!"