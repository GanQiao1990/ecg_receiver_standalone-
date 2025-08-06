#!/bin/bash

# ECG AI诊断项目 - ARM Linux开发板安装脚本
# 支持: Raspberry Pi, Jetson Nano, Orange Pi, Rock Pi等

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"  
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印横幅
print_banner() {
    echo "=========================================================================="
    echo "🫀 ECG AI心脏诊断项目 - ARM Linux开发板安装程序"
    echo "=========================================================================="
    echo "支持平台: Raspberry Pi, Jetson Nano, Orange Pi, Rock Pi"
    echo "系统要求: Ubuntu/Debian Linux on ARM64/ARMv7"
    echo "=========================================================================="
    echo ""
}

# 检测系统信息
detect_system() {
    print_status "检测系统信息..."
    
    # 检测架构
    ARCH=$(uname -m)
    print_status "CPU架构: $ARCH"
    
    # 检测发行版
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VERSION=$VERSION_ID
        print_status "操作系统: $OS $VERSION"
    else
        print_error "无法检测操作系统版本"
        exit 1
    fi
    
    # 检测开发板类型
    if [ -f /proc/device-tree/model ]; then
        BOARD=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || echo "未知")
        print_status "开发板: $BOARD"
    else
        BOARD="未知ARM设备"
        print_status "开发板: $BOARD"
    fi
    
    # 检测内存
    MEMORY=$(free -h | awk '/^Mem:/ {print $2}')
    print_status "可用内存: $MEMORY"
    
    # 检测存储空间
    STORAGE=$(df -h / | awk 'NR==2 {print $4}')
    print_status "可用存储: $STORAGE"
    
    echo ""
}

# 检查系统兼容性
check_compatibility() {
    print_status "检查系统兼容性..."
    
    # 检查架构兼容性
    case $ARCH in
        aarch64|arm64)
            print_success "ARM64架构 - 完全兼容"
            ;;
        armv7l|armhf)
            print_warning "ARM32架构 - 基本兼容，性能可能有限"
            ;;
        *)
            print_error "不支持的CPU架构: $ARCH"
            print_error "项目需要ARM架构处理器"
            exit 1
            ;;
    esac
    
    # 检查内存要求
    MEMORY_MB=$(free -m | awk '/^Mem:/ {print $2}')
    if [ $MEMORY_MB -lt 2048 ]; then
        print_error "内存不足: ${MEMORY_MB}MB < 2048MB"
        print_error "建议至少4GB内存以获得最佳性能"
        exit 1
    elif [ $MEMORY_MB -lt 4096 ]; then
        print_warning "内存: ${MEMORY_MB}MB，建议4GB以上"
    else
        print_success "内存充足: ${MEMORY_MB}MB"
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        print_status "Python版本: $PYTHON_VERSION"
        
        if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
            print_error "Python版本过低: $PYTHON_VERSION < 3.8"
            exit 1
        fi
    else
        print_error "未找到Python3"
        exit 1
    fi
    
    echo ""
}

# 优化系统性能
optimize_system() {
    print_status "优化系统性能..."
    
    # 检查是否为树莓派
    if [[ $BOARD == *"Raspberry Pi"* ]]; then
        print_status "检测到树莓派，应用专用优化..."
        
        # GPU内存分配
        if ! grep -q "gpu_mem=" /boot/config.txt; then
            echo "gpu_mem=128" | sudo tee -a /boot/config.txt > /dev/null
            print_success "设置GPU内存: 128MB"
        fi
        
        # 启用相机接口（如果需要）
        sudo raspi-config nonint do_camera 0 2>/dev/null || true
        
        # 启用串口（ESP32连接需要）
        sudo raspi-config nonint do_serial 0 2>/dev/null || true
        print_success "启用串口通信"
    fi
    
    # 检查是否为Jetson设备
    if [[ $BOARD == *"Jetson"* ]] || command -v jetson_clocks &> /dev/null; then
        print_status "检测到Jetson设备，应用专用优化..."
        
        # 设置最大性能模式
        if command -v jetson_clocks &> /dev/null; then
            sudo jetson_clocks || print_warning "无法设置Jetson性能模式"
            print_success "启用Jetson最大性能模式"
        fi
    fi
    
    # 通用性能优化
    # 设置CPU调度器为性能模式
    if [ -d /sys/devices/system/cpu/cpu0/cpufreq ]; then
        echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1 || true
        print_success "设置CPU性能模式"
    fi
    
    # 增加交换文件（如果内存不足）
    if [ $MEMORY_MB -lt 4096 ]; then
        if [ ! -f /swapfile ]; then
            print_status "内存不足4GB，创建2GB交换文件..."
            sudo fallocate -l 2G /swapfile
            sudo chmod 600 /swapfile
            sudo mkswap /swapfile
            sudo swapon /swapfile
            echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab > /dev/null
            print_success "创建2GB交换文件"
        fi
    fi
    
    echo ""
}

# 更新系统包
update_system() {
    print_status "更新系统包..."
    
    # 更新包索引
    sudo apt update -y
    
    # 升级已安装的包（可选）
    read -p "是否升级系统包？这可能需要较长时间 (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "升级系统包..."
        sudo apt upgrade -y
        print_success "系统包升级完成"
    else
        print_status "跳过系统包升级"
    fi
    
    echo ""
}

# 安装系统依赖
install_system_dependencies() {
    print_status "安装系统依赖包..."
    
    # 基础开发工具
    sudo apt install -y \
        build-essential \
        cmake \
        pkg-config \
        git \
        wget \
        curl \
        unzip \
        software-properties-common
    
    # Python开发环境
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-dev \
        python3-venv \
        python3-setuptools
    
    # Qt5开发库（ARM优化版本）
    sudo apt install -y \
        qtbase5-dev \
        qttools5-dev \
        qt5-qmake \
        qtbase5-dev-tools
    
    # 图形界面相关
    if [ "$XDG_SESSION_TYPE" != "tty" ]; then
        sudo apt install -y \
            libqt5gui5 \
            libqt5widgets5 \
            libqt5core5a \
            libfontconfig1-dev \
            libfreetype6-dev \
            libx11-dev \
            libxext-dev \
            libxfixes-dev \
            libxi-dev \
            libxrender-dev \
            libxcb1-dev \
            libx11-xcb-dev \
            libxcb-glx0-dev
    fi
    
    # 串口通信支持
    sudo apt install -y \
        minicom \
        setserial
    
    # 数学和科学计算库
    sudo apt install -y \
        libatlas-base-dev \
        libblas-dev \
        liblapack-dev \
        gfortran
    
    print_success "系统依赖安装完成"
    echo ""
}

# 安装Python依赖
install_python_dependencies() {
    print_status "安装Python依赖包..."
    
    # 升级pip
    python3 -m pip install --upgrade pip
    
    # 为ARM平台优化的包安装
    print_status "安装核心Python包..."
    
    # 安装numpy（优化版本）
    if [[ $ARCH == "aarch64" ]]; then
        # ARM64使用预编译轮子
        python3 -m pip install numpy==1.24.3
    else
        # ARM32可能需要编译
        python3 -m pip install numpy>=1.21.0
    fi
    
    # 安装其他数值计算包
    python3 -m pip install scipy>=1.9.0
    
    # 安装串口通信
    python3 -m pip install pyserial>=3.5
    
    # 安装网络请求
    python3 -m pip install requests>=2.28.0
    
    # 安装配置管理
    python3 -m pip install python-dotenv>=1.0.0
    
    print_success "核心Python包安装完成"
    
    # PyQt5安装（最复杂的部分）
    print_status "安装PyQt5和pyqtgraph..."
    
    # 首先尝试从系统包安装PyQt5
    if sudo apt list --installed 2>/dev/null | grep -q python3-pyqt5; then
        print_success "PyQt5已从系统包安装"
    else
        # 尝试安装系统版本的PyQt5
        sudo apt install -y python3-pyqt5 python3-pyqt5-dev python3-pyqt5.qttools || {
            print_warning "系统包安装失败，尝试pip安装..."
            
            # 尝试pip安装
            if [[ $ARCH == "aarch64" ]]; then
                # ARM64通常有预编译轮子
                python3 -m pip install PyQt5>=5.15.0
            else
                # ARM32可能需要较长编译时间
                print_warning "ARM32架构安装PyQt5可能需要很长时间..."
                python3 -m pip install PyQt5>=5.12.0 --no-cache-dir
            fi
        }
    fi
    
    # 安装pyqtgraph
    python3 -m pip install pyqtgraph>=0.13.0
    
    print_success "PyQt5安装完成"
    echo ""
}

# 配置串口权限
setup_serial_permissions() {
    print_status "配置串口访问权限..."
    
    # 将当前用户添加到dialout组
    sudo usermod -a -G dialout $USER
    
    # 设置串口设备权限
    if [ -c /dev/ttyUSB0 ]; then
        sudo chmod 666 /dev/ttyUSB0
    fi
    
    if [ -c /dev/ttyACM0 ]; then
        sudo chmod 666 /dev/ttyACM0
    fi
    
    print_success "串口权限配置完成"
    print_warning "需要重新登录或重启系统以使权限生效"
    echo ""
}

# 安装ECG诊断项目
install_ecg_project() {
    print_status "安装ECG诊断项目..."
    
    # 检查项目文件
    if [ ! -f "ecg_diagnosis.py" ]; then
        print_error "未找到ECG诊断项目文件"
        print_error "请确保在项目根目录运行此脚本"
        exit 1
    fi
    
    # 创建虚拟环境（推荐）
    read -p "是否创建Python虚拟环境？(推荐) (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        print_status "创建虚拟环境..."
        python3 -m venv ecg_env
        source ecg_env/bin/activate
        print_success "虚拟环境创建完成"
    fi
    
    # 配置环境变量
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "创建配置文件.env"
        print_warning "请编辑.env文件添加您的Gemini API密钥"
    fi
    
    print_success "ECG项目配置完成"
    echo ""
}

# 测试安装
test_installation() {
    print_status "测试安装..."
    
    # 测试Python导入
    python3 -c "
import sys
print(f'Python版本: {sys.version}')

try:
    import numpy
    print('✅ numpy导入成功')
except ImportError as e:
    print(f'❌ numpy导入失败: {e}')
    sys.exit(1)

try:
    import serial
    print('✅ pyserial导入成功')
except ImportError as e:
    print(f'❌ pyserial导入失败: {e}')
    sys.exit(1)

try:
    from PyQt5.QtWidgets import QApplication
    print('✅ PyQt5导入成功')
except ImportError as e:
    print(f'❌ PyQt5导入失败: {e}')
    sys.exit(1)

try:
    import pyqtgraph
    print('✅ pyqtgraph导入成功')
except ImportError as e:
    print(f'❌ pyqtgraph导入失败: {e}')
    sys.exit(1)

try:
    import requests
    print('✅ requests导入成功')
except ImportError as e:
    print(f'❌ requests导入失败: {e}')
    sys.exit(1)

print('\\n🎉 所有依赖包测试通过！')
"
    
    if [ $? -eq 0 ]; then
        print_success "依赖包测试通过"
        
        # 测试ECG诊断模块
        if [ -f "ecg_diagnosis.py" ]; then
            python3 -c "
try:
    from ecg_diagnosis import GeminiECGDiagnosisClient
    print('✅ ECG诊断模块导入成功')
except ImportError as e:
    print(f'❌ ECG诊断模块导入失败: {e}')
" 2>/dev/null && print_success "ECG诊断模块测试通过" || print_warning "ECG诊断模块测试失败"
        fi
    else
        print_error "依赖包测试失败"
        exit 1
    fi
    
    echo ""
}

# 显示完成信息
show_completion_info() {
    echo "=========================================================================="
    print_success "🎉 ECG AI诊断项目安装完成！"
    echo "=========================================================================="
    echo ""
    print_status "下一步操作:"
    echo "1. 🔑 获取Gemini API密钥: https://api.gptnb.ai/"
    echo "2. 📝 编辑.env文件，添加API密钥"
    echo "3. 🔌 连接ESP32 ECG设备到开发板"
    echo "4. 🚀 运行应用程序:"
    echo ""
    echo "   # 测试诊断功能（无需硬件）"
    echo "   python3 test_diagnosis.py"
    echo ""
    echo "   # 启动完整应用程序"
    echo "   python3 -m ecg_receiver.main"
    echo ""
    print_status "系统信息:"
    echo "• 开发板: $BOARD"
    echo "• 架构: $ARCH"
    echo "• 内存: $MEMORY"
    echo "• 存储: $STORAGE"
    echo ""
    print_status "文档资源:"
    echo "• README.md - 使用说明"
    echo "• LINUX_BOARDS_CN.md - Linux开发板指南"
    echo "• DEPLOYMENT.md - 部署文档"
    echo ""
    print_warning "重要提醒:"
    echo "• 如果使用串口，请重新登录以使权限生效"
    echo "• 建议重启开发板以应用所有优化设置"
    echo "• 确保网络连接正常以使用AI诊断功能"
    echo ""
    echo "=========================================================================="
}

# 主函数
main() {
    print_banner
    detect_system
    check_compatibility
    
    # 确认安装
    read -p "是否继续安装ECG AI诊断项目？ (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_status "安装已取消"
        exit 0
    fi
    
    optimize_system
    update_system
    install_system_dependencies
    install_python_dependencies
    setup_serial_permissions
    install_ecg_project
    test_installation
    show_completion_info
}

# 错误处理
trap 'print_error "安装过程中发生错误，请检查上述输出"; exit 1' ERR

# 运行主函数
main "$@"