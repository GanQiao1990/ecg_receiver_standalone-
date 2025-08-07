# Tkinter Designer Integration Guide for ECG AI Diagnosis

## 🎨 **使用Tkinter Designer重新设计GUI的完整指南**

这份指南将帮助您使用[Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer)工具，将Figma设计直接转换为Python Tkinter代码。

## 📋 **步骤概览**

### **Phase 1: Figma设计 (1-2天)**
1. 创建Figma设计文件
2. 设计现代化ECG界面
3. 定义交互状态
4. 导出设计token

### **Phase 2: Tkinter Designer转换 (1天)**
1. 安装Tkinter Designer
2. 获取Figma API token
3. 转换设计为Tkinter代码
4. 集成生成的GUI代码

### **Phase 3: 功能集成 (2-3天)**
1. 连接ECG诊断逻辑
2. 实现数据绑定
3. 添加实时更新
4. 测试完整功能

---

## 🎯 **详细实施步骤**

### **步骤1: 设置Figma设计**

#### **1.1 创建Figma项目**
```
项目名称: ECG AI Diagnosis - Modern UI
画布尺寸: 1400 x 900px (Desktop)
设计系统: 基于医疗设备专业风格
```

#### **1.2 设计规范**
```css
/* 颜色方案 */
Primary: #1e3a8a (Deep Blue)
Secondary: #3b82f6 (Standard Blue)
Background: #0f172a (Dark)
Cards: #1e293b (Card Background)
Success: #10b981 (Green)
Warning: #f59e0b (Yellow)
Error: #ef4444 (Red)

/* 字体规范 */
Font Family: "Segoe UI", sans-serif
Title: 24px, Bold
Heading: 18px, Bold  
Body: 12px, Regular
Small: 10px, Regular

/* 间距系统 */
XS: 4px
SM: 8px
MD: 16px
LG: 24px
XL: 32px

/* 圆角规范 */
Small: 6px (inputs, small buttons)
Medium: 8px (buttons, small cards)
Large: 12px (main cards)
XL: 16px (main containers)
```

### **步骤2: Figma界面设计**

#### **2.1 主界面布局**
```
Header (1400 x 80px)
├── Logo + Title (左侧)
├── Settings Button (右侧)
└── Help Button (右侧)

Main Content (1400 x 720px)
├── ECG Monitor Panel (840 x 720px)
│   ├── ECG Plot Area (800 x 400px)
│   ├── Control Panel (800 x 160px)
│   └── Statistics Panel (800 x 160px)
└── AI Diagnosis Panel (560 x 720px)
    ├── API Config (520 x 120px)
    ├── Patient Info (520 x 120px)
    ├── Diagnosis Control (520 x 100px)
    └── Results Display (520 x 380px)

Footer (1400 x 40px)
├── Status Info (左侧)
└── Version Info (右侧)
```

#### **2.2 组件设计清单**

**按钮组件**:
```
□ Primary Button (Connect, Analyze ECG)
□ Secondary Button (Refresh, Settings)
□ Success Button (Start Recording)
□ Warning Button (Stop Recording)
□ Danger Button (Disconnect, Emergency)
```

**卡片组件**:
```
□ Main Panel Card (ECG Monitor, AI Diagnosis)
□ Sub Panel Card (Controls, Statistics, Config)
□ Result Card (Diagnosis Results)
□ Status Card (Connection Status, API Status)
```

**表单组件**:
```
□ Text Input (API Key, Patient Info)
□ Dropdown/ComboBox (Port Selection, Gender)
□ Progress Bar (Diagnosis Progress)
□ Status Indicator (Connection Status)
```

**图表组件**:
```
□ ECG Plot Container (实时波形显示区域)
□ Statistics Grid (心率、信号质量等)
□ Diagnosis History List
```

### **步骤3: 安装和配置Tkinter Designer**

#### **3.1 安装Tkinter Designer**
```bash
# 方法1: 从GitHub安装
git clone https://github.com/ParthJadhav/Tkinter-Designer.git
cd Tkinter-Designer
pip install -r requirements.txt

# 方法2: 使用pip安装 (如果可用)
pip install tkinter-designer
```

#### **3.2 获取Figma API Token**
```
1. 登录Figma.com
2. 进入 Settings > Account > Personal Access Tokens
3. 点击 "Create a new personal access token"
4. 命名: "ECG-Designer-Token"
5. 复制生成的token (保密!)
```

#### **3.3 获取Figma File URL**
```
1. 在Figma中打开你的设计文件
2. 复制浏览器地址栏中的URL
3. 格式: https://www.figma.com/file/[FILE-ID]/[FILE-NAME]
4. 提取FILE-ID (斜杠之间的长字符串)
```

### **步骤4: 生成Tkinter代码**

#### **4.1 运行Tkinter Designer**
```bash
# 进入Tkinter Designer目录
cd Tkinter-Designer

# 运行GUI工具
python gui.py

# 或使用命令行
python cli.py [FIGMA-FILE-URL] [FIGMA-TOKEN]
```

#### **4.2 配置生成选项**
```
输入信息:
- Figma File URL: [你的设计文件URL]
- Figma Token: [你的API token]
- Output Path: ./output/ecg_gui

选项:
☑️ Generate GUI Code
☑️ Download Images
☑️ Create Assets Folder
```

#### **4.3 生成的文件结构**
```
output/ecg_gui/
├── gui.py              # 主GUI代码
├── assets/             # 图片资源
│   ├── images/
│   └── icons/
└── build/              # 构建文件
```

### **步骤5: 集成生成的GUI**

#### **5.1 移动生成的文件**
```bash
# 复制生成的GUI代码到项目
cp output/ecg_gui/gui.py ecg_receiver/gui_tkinter/generated_gui.py
cp -r output/ecg_gui/assets ecg_receiver/gui_tkinter/

# 创建集成文件
touch ecg_receiver/gui_tkinter/integrated_main.py
```

#### **5.2 集成现有功能**
```python
# integrated_main.py 示例
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# 导入生成的GUI
from .generated_gui import *
from .main_window_modern import ModernECGMainWindow

class FigmaIntegratedECGWindow(ModernECGMainWindow):
    """集成Figma设计的ECG主窗口"""
    
    def __init__(self):
        # 使用生成的GUI布局
        super().__init__()
        self.setup_figma_layout()
        
    def setup_figma_layout(self):
        """使用Figma生成的布局"""
        # 这里集成generated_gui.py中的布局代码
        pass
        
    # 保留原有的功能方法
    # scan_ports, toggle_connection, etc.
```

### **步骤6: 优化和定制**

#### **6.1 修复自动生成的代码**
```python
# 常见需要修复的问题:

# 1. 添加导入语句
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter

# 2. 修复图像路径
def relative_to_assets(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), "assets", path)

# 3. 添加事件绑定
button.configure(command=self.your_callback_function)

# 4. 集成实时数据更新
def update_ecg_plot(self, data):
    # 更新matplotlib图表
    pass
```

#### **6.2 添加响应式设计**
```python
def configure_responsive_layout(self):
    """配置响应式布局"""
    # 添加权重配置
    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    
    # 最小尺寸设置
    self.root.minsize(1200, 700)
```

### **步骤7: 测试和优化**

#### **7.1 功能测试清单**
```
GUI测试:
□ 窗口正常显示和响应
□ 按钮点击事件正确绑定
□ 输入框数据获取正常
□ 状态指示器更新正确

集成测试:
□ 串口连接功能正常
□ ECG数据显示实时更新
□ AI诊断功能正常工作
□ 数据录制功能正常

性能测试:
□ 界面响应速度良好
□ 内存使用合理
□ CPU占用率正常
□ 跨平台兼容性
```

#### **7.2 用户体验优化**
```
视觉优化:
□ 颜色对比度符合标准
□ 字体大小易于阅读
□ 图标清晰可辨识
□ 动画效果流畅

交互优化:
□ 按钮状态反馈及时
□ 错误提示友好明确
□ 快捷键支持
□ 无障碍访问支持
```

---

## 🚀 **快速开始指南**

### **如果您想立即尝试现代化GUI:**

```bash
# 1. 安装新依赖
pip install customtkinter matplotlib Pillow

# 2. 运行现代化GUI
python launch_modern_gui.py

# 3. 对比原版GUI
python -m ecg_receiver.main  # 原PyQt5版本
```

### **当前实现状态:**
✅ **已完成**:
- 现代化的CustomTkinter GUI框架
- 专业医疗设备风格设计
- 完整的颜色系统和组件库
- ECG实时波形显示
- AI诊断面板集成
- 响应式布局设计

🔄 **进行中**:
- Figma设计文件创建
- Tkinter Designer集成测试
- 高级动画效果实现

📋 **待完成**:
- 完整的Figma设计转换
- 自定义主题切换功能
- 移动端适配版本

---

## 💡 **设计理念**

### **现代医疗设备界面设计原则**:
1. **专业性** - 深色主题，减少眼部疲劳
2. **清晰性** - 高对比度，重要信息突出显示
3. **直观性** - 符合医疗人员使用习惯
4. **响应式** - 适应不同屏幕尺寸
5. **可靠性** - 稳定的状态指示和错误处理

### **相比原PyQt5 GUI的改进**:
- 🎨 **更现代的视觉设计** - 医疗级专业外观
- 🚀 **更好的性能** - CustomTkinter优化渲染
- 📱 **响应式布局** - 适配不同分辨率
- 🔧 **更易维护** - 模块化组件设计
- 🎯 **更好的用户体验** - 直观的操作流程

**现在您就可以体验全新的现代化ECG AI诊断界面！** 🫀✨