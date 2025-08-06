#!/bin/bash

# 树莓派ECG AI诊断项目优化脚本
# 专为Raspberry Pi 4B/5优化

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_info "🍓 树莓派ECG AI诊断项目优化配置"
print_info "适用于: Raspberry Pi 4B/5 with 4GB/8GB RAM"
echo "================================================================"

# 检测树莓派型号
PI_MODEL=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || echo "Unknown")
print_info "检测到设备: $PI_MODEL"

# 检查是否为树莓派
if [[ ! $PI_MODEL == *"Raspberry Pi"* ]]; then
    print_error "此脚本仅适用于树莓派设备"
    exit 1
fi

# 1. 系统配置优化
print_info "正在优化系统配置..."

# 备份原始配置
sudo cp /boot/config.txt /boot/config.txt.backup.$(date +%Y%m%d)

# GPU内存分配 (为GUI界面优化)
if ! grep -q "gpu_mem=" /boot/config.txt; then
    echo "gpu_mem=256" | sudo tee -a /boot/config.txt
    print_info "设置GPU内存: 256MB (GUI优化)"
fi

# 启用硬件加速
if ! grep -q "dtoverlay=vc4-kms-v3d" /boot/config.txt; then
    echo "dtoverlay=vc4-kms-v3d" | sudo tee -a /boot/config.txt
    print_info "启用硬件3D加速"
fi

# CPU超频 (仅Pi 4B)
if [[ $PI_MODEL == *"Raspberry Pi 4"* ]]; then
    if ! grep -q "arm_freq=" /boot/config.txt; then
        echo "arm_freq=1800" | sudo tee -a /boot/config.txt
        echo "over_voltage=4" | sudo tee -a /boot/config.txt
        print_info "设置CPU频率: 1.8GHz (轻度超频)"
        print_warn "请确保有良好散热"
    fi
fi

# 启用串口 (ESP32通信)
sudo raspi-config nonint do_serial 0
print_info "启用串口通信 (ESP32连接)"

# 启用I2C和SPI (扩展传感器支持)
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
print_info "启用I2C和SPI接口"

# 2. 内存优化
print_info "优化内存配置..."

# 检查内存大小
MEMORY_GB=$(free -h | awk '/^Mem:/ {print $2}' | sed 's/Gi*//')
print_info "可用内存: ${MEMORY_GB}GB"

# 如果内存小于4GB，创建交换文件
if [ ${MEMORY_GB%.*} -lt 4 ]; then
    if [ ! -f /swapfile ]; then
        print_info "内存不足4GB，创建2GB交换文件..."
        sudo fallocate -l 2G /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
        print_info "交换文件创建完成"
    fi
else
    print_info "内存充足，无需额外交换文件"
fi

# 3. 存储优化
print_info "优化存储性能..."

# SD卡超频
if ! grep -q "dtparam=sd_overclock=" /boot/config.txt; then
    echo "dtparam=sd_overclock=100" | sudo tee -a /boot/config.txt
    print_info "启用SD卡超频: 100MHz"
fi

# 推荐使用SSD
print_warn "建议使用USB 3.0 SSD替代SD卡以获得更好性能"
print_info "SSD设置指南: https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md"

# 4. 网络优化
print_info "优化网络配置..."

# WiFi国家代码设置
sudo raspi-config nonint do_wifi_country CN
print_info "设置WiFi国家代码: CN"

# 5. 串口设备权限
print_info "配置串口设备权限..."

# 添加用户到相关组
sudo usermod -a -G dialout,gpio,i2c,spi $USER
print_info "添加用户到硬件访问组"

# 设置串口设备权限
sudo tee /etc/udev/rules.d/99-ecg-serial.rules > /dev/null <<EOF
# ESP32 ECG设备权限
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", GROUP="dialout"
EOF

print_info "配置ESP32设备权限规则"

# 6. Python环境优化
print_info "优化Python环境..."

# 安装树莓派优化的Python包
sudo apt update
sudo apt install -y python3-numpy python3-scipy python3-matplotlib

# 7. 显示优化
print_info "配置显示设置..."

# HDMI强制输出 (避免检测问题)
if ! grep -q "hdmi_force_hotplug=1" /boot/config.txt; then
    echo "hdmi_force_hotplug=1" | sudo tee -a /boot/config.txt
    print_info "启用HDMI强制输出"
fi

# 设置合适的分辨率
if ! grep -q "hdmi_mode=" /boot/config.txt; then
    echo "hdmi_mode=82" | sudo tee -a /boot/config.txt  # 1920x1080 60Hz
    print_info "设置HDMI分辨率: 1920x1080@60Hz"
fi

# 8. 性能监控设置
print_info "设置性能监控..."

# 创建性能监控脚本
sudo tee /usr/local/bin/pi-monitor > /dev/null <<'EOF'
#!/bin/bash
# 树莓派性能监控脚本

echo "=================== 树莓派性能状态 ==================="
echo "时间: $(date)"
echo ""

# CPU信息
echo "🔥 CPU温度: $(vcgencmd measure_temp | cut -d= -f2)"
echo "⚡ CPU频率: $(vcgencmd measure_clock arm | cut -d= -f2 | awk '{printf "%.0f MHz\n", $1/1000000}')"
echo "📊 CPU使用率: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')"

# 内存信息
echo ""
echo "💾 内存使用:"
free -h | grep -E "(Mem|Swap)"

# 存储信息
echo ""
echo "💽 存储使用:"
df -h / | tail -1 | awk '{print "根分区: " $3 "/" $2 " (" $5 " 已使用)"}'

# GPU信息
echo ""
echo "🎮 GPU内存: $(vcgencmd get_mem gpu | cut -d= -f2)"

# 网络信息
echo ""
echo "🌐 网络状态:"
ip route get 8.8.8.8 | head -1 | cut -d' ' -f7 | xargs -I {} ip addr show {} | grep inet | head -1 | awk '{print "IP地址: " $2}'

echo "======================================================"
EOF

sudo chmod +x /usr/local/bin/pi-monitor
print_info "创建性能监控脚本: pi-monitor"

# 9. ECG项目特定优化
print_info "应用ECG项目特定优化..."

# 设置实时优先级 (提高数据采集稳定性)
echo "@$USER - rtprio 99" | sudo tee -a /etc/security/limits.conf
echo "@$USER - nice -10" | sudo tee -a /etc/security/limits.conf
print_info "设置实时进程优先级"

# 10. 服务优化
print_info "优化系统服务..."

# 禁用不必要的服务以节省资源
SERVICES_TO_DISABLE=(
    "bluetooth.service"
    "hciuart.service"  
    "avahi-daemon.service"
    "triggerhappy.service"
)

for service in "${SERVICES_TO_DISABLE[@]}"; do
    if systemctl is-enabled "$service" &>/dev/null; then
        read -p "禁用 $service 服务以节省资源？ (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo systemctl disable "$service"
            print_info "已禁用: $service"
        fi
    fi
done

# 11. 创建启动脚本
print_info "创建ECG应用启动脚本..."

tee ~/start_ecg.sh > /dev/null <<'EOF'
#!/bin/bash
# ECG AI诊断应用启动脚本

cd ~/ecm_llm  # 修改为您的项目路径

echo "🫀 启动ECG AI诊断应用..."
echo "请确保："
echo "1. ✅ ESP32设备已连接"
echo "2. ✅ 网络连接正常"
echo "3. ✅ API密钥已配置"
echo ""

# 显示系统状态
pi-monitor

echo ""
read -p "按回车键启动应用..."

# 启动应用
python3 -m ecg_receiver.main
EOF

chmod +x ~/start_ecg.sh
print_info "创建启动脚本: ~/start_ecg.sh"

# 12. 创建桌面快捷方式
if [ "$XDG_SESSION_TYPE" != "tty" ]; then
    print_info "创建桌面快捷方式..."
    
    mkdir -p ~/Desktop
    tee ~/Desktop/ECG-AI-Diagnosis.desktop > /dev/null <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ECG AI Diagnosis
Comment=ECG心电图AI诊断系统
Exec=/home/$USER/start_ecg.sh
Icon=applications-science
Terminal=true
Categories=Science;Medical;Education;
StartupNotify=true
EOF
    
    chmod +x ~/Desktop/ECG-AI-Diagnosis.desktop
    print_info "桌面快捷方式创建完成"
fi

# 完成信息
echo ""
echo "================================================================"
print_info "🎉 树莓派ECG AI诊断项目优化完成！"
echo "================================================================"
echo ""
print_info "已完成的优化:"
echo "✅ GPU内存分配: 256MB"
echo "✅ 硬件3D加速启用"
echo "✅ 串口、I2C、SPI接口启用"
echo "✅ 存储和网络优化" 
echo "✅ 用户权限配置"
echo "✅ 性能监控工具"
echo "✅ 启动脚本和桌面快捷方式"
echo ""
print_warn "重要提醒:"
echo "• 🔄 请重启树莓派以应用所有配置更改"
echo "• 🌡️ 监控CPU温度，确保散热良好"
echo "• 🔌 重新登录以使用户组权限生效"
echo ""
print_info "快捷命令:"
echo "• 性能监控: pi-monitor"
echo "• 启动ECG应用: ~/start_ecg.sh"
echo "• 桌面快捷方式: 双击桌面图标"
echo ""
print_info "如需重启: sudo reboot"
echo "================================================================"