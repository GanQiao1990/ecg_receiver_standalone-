# ECG AI诊断系统 - Tkinter Designer GUI重设计方案

## 🎨 设计理念

### 现代化设计特点
- **扁平化设计** - 简洁现代的视觉风格
- **深色主题** - 专业医疗设备风格
- **卡片式布局** - 清晰的功能分区
- **渐变效果** - 增加视觉层次
- **圆角设计** - 柔和的用户体验
- **动效反馈** - 提升交互体验

### 配色方案
```python
# 主色调 - 医疗蓝
PRIMARY_BLUE = "#1e3a8a"      # 深蓝色
SECONDARY_BLUE = "#3b82f6"    # 标准蓝
LIGHT_BLUE = "#93c5fd"        # 浅蓝色

# 背景色
BG_DARK = "#0f172a"           # 深色背景
BG_CARD = "#1e293b"           # 卡片背景
BG_LIGHT = "#334155"          # 浅色背景

# 文本色
TEXT_WHITE = "#ffffff"        # 主要文本
TEXT_GRAY = "#94a3b8"         # 次要文本
TEXT_ACCENT = "#fbbf24"       # 强调文本

# 状态色
SUCCESS_GREEN = "#10b981"     # 成功
WARNING_YELLOW = "#f59e0b"    # 警告
ERROR_RED = "#ef4444"         # 错误
CRITICAL_RED = "#dc2626"      # 严重
```

## 📱 界面布局设计

### 整体布局 (1400x900)
```
┌─────────────────────────────────────────────────────────┐
│ 🫀 ECG AI Heart Diagnosis          [Settings] [Help] │ Header (80px)
├─────────────────────────────────────────────────────────┤
│ ┌─ ECG Monitor ────┐ ┌─ AI Diagnosis ──────────────┐ │
│ │                  │ │ ┌─ API Config ──────────┐   │ │
│ │   ╭─────────────╮ │ │ │ API Key: [________]   │   │ │
│ │   │             │ │ │ │ Status: ●Connected    │   │ │
│ │   │ ECG波形图    │ │ │ └──────────────────────┘   │ │
│ │   │   实时显示   │ │ │                            │ │
│ │   │             │ │ │ ┌─ Patient Info ────────┐   │ │ Main Content (720px)
│ │   ╰─────────────╯ │ │ │ Age: [__] Gender: [_] │   │ │
│ │                  │ │ │ Symptoms: [_________] │   │ │
│ │ ┌─ Controls ───┐ │ │ └──────────────────────┘   │ │
│ │ │ Port: [___▼] │ │ │                            │ │
│ │ │ [Connect]    │ │ │ ┌─ Diagnosis Results ───┐   │ │
│ │ │ [Record]     │ │ │ │ ┌Current┐┌History┐    │   │ │
│ │ └──────────────┘ │ │ │ │       ││       │    │   │ │
│ └──────────────────┘ │ │ │       ││       │    │   │ │
│                      │ │ └───────┴┴───────┘    │   │ │
│                      │ │ [Analyze ECG] [Auto]   │   │ │
│                      │ └────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Status: Connected | HR: 75 BPM | Last: 2min ago      │ Footer (40px)
└─────────────────────────────────────────────────────────┘
```

### 功能模块设计

#### 1. 头部导航 (Header)
- 应用Logo和标题
- 设置按钮 (API配置、主题切换)
- 帮助按钮 (使用指南)
- 最小化/关闭按钮

#### 2. ECG监控面板 (左侧 60%)
- **实时波形图**：matplotlib集成，显示ECG波形
- **控制面板**：串口选择、连接/断开、录制开关
- **实时统计**：心率、信号质量、数据计数

#### 3. AI诊断面板 (右侧 40%)
- **API配置**：密钥输入、连接状态
- **患者信息**：年龄、性别、症状输入
- **诊断结果**：标签页显示当前/历史诊断
- **操作按钮**：手动诊断、自动诊断开关

#### 4. 状态栏 (Footer)
- 连接状态、心率显示、最近诊断时间
- 进度指示器、错误提示

## 🎯 Figma设计文件结构

### 页面结构
```
ECG AI Diagnosis App
├── Desktop - Main (1400x900)
├── Desktop - Settings Dialog  
├── Desktop - Help Dialog
├── Desktop - Error States
└── Components
    ├── Buttons
    ├── Cards
    ├── Form Elements
    ├── Charts
    └── Status Indicators
```

### 组件设计规范
```python
# 按钮样式
BUTTON_PRIMARY = {
    "bg": PRIMARY_BLUE,
    "fg": TEXT_WHITE,
    "border_radius": 8,
    "padding": (12, 24),
    "font": ("Segoe UI", 11, "bold")
}

BUTTON_SECONDARY = {
    "bg": BG_LIGHT, 
    "fg": TEXT_WHITE,
    "border": f"1px solid {SECONDARY_BLUE}",
    "border_radius": 8
}

# 卡片样式
CARD_STYLE = {
    "bg": BG_CARD,
    "border_radius": 12,
    "shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "padding": 16
}

# 输入框样式  
INPUT_STYLE = {
    "bg": BG_LIGHT,
    "fg": TEXT_WHITE,
    "border": f"1px solid {TEXT_GRAY}",
    "border_radius": 6,
    "padding": (8, 12)
}
```

## 🔧 技术实现方案

### 依赖包更新
```python
# 新增tkinter相关依赖
customtkinter>=5.2.0      # 现代化tkinter组件
matplotlib>=3.7.0         # 图表绘制
tkdesigner>=1.0.7   # Figma到tkinter转换工具
Pillow>=10.0.0           # 图像处理
```

### 文件结构
```
ecg_receiver/
├── gui_tkinter/              # 新的tkinter GUI模块
│   ├── __init__.py
│   ├── main_window.py        # 主窗口
│   ├── components/           # UI组件
│   │   ├── ecg_plot.py      # ECG波形图组件
│   │   ├── diagnosis_panel.py # 诊断面板
│   │   ├── control_panel.py  # 控制面板
│   │   └── dialogs.py       # 对话框
│   ├── assets/              # 设计资源
│   │   ├── images/          # 图标和图片
│   │   ├── fonts/           # 字体文件
│   │   └── gui.py           # Tkinter Designer生成的文件
│   └── styles/              # 样式定义
│       ├── colors.py        # 颜色定义
│       ├── fonts.py         # 字体定义
│       └── themes.py        # 主题配置
├── gui/                     # 原PyQt5 GUI (保留)
└── main_tkinter.py          # Tkinter版本入口
```

## 📐 Figma设计步骤

### Step 1: 创建Figma文件
1. 创建新的Figma设计文件
2. 设置画布尺寸: 1400x900px
3. 创建组件库和样式系统

### Step 2: 设计主界面
1. 绘制整体布局框架
2. 设计ECG波形展示区域
3. 创建诊断面板UI
4. 设计控制按钮和表单

### Step 3: 定义交互状态
1. 按钮hover/active状态
2. 输入框focus状态  
3. 加载和错误状态
4. 成功和警告提示

### Step 4: 导出设计
1. 导出所有图像资源
2. 生成CSS样式
3. 创建组件规范文档

## 🚀 实现优势

### 相比PyQt5的优势
✅ **更轻量** - tkinter是Python标准库，无需额外安装  
✅ **更现代** - 使用CustomTkinter获得现代化外观  
✅ **更灵活** - Figma设计直接转换为代码  
✅ **更易维护** - 视觉设计与代码分离  
✅ **更好兼容** - 在所有平台上表现一致  

### 新功能增强
🎨 **主题切换** - 支持亮色/暗色主题  
📱 **响应式布局** - 适配不同屏幕尺寸  
🎯 **快捷操作** - 键盘快捷键支持  
💫 **动画效果** - 平滑的界面过渡  
🔔 **通知系统** - 诊断完成通知  

## 📋 实施计划

### Phase 1: 设计阶段 (1-2天)
- [ ] 创建Figma设计文件
- [ ] 设计主界面布局
- [ ] 定义组件样式规范
- [ ] 完成交互状态设计

### Phase 2: 转换阶段 (2-3天)  
- [ ] 使用Tkinter Designer转换设计
- [ ] 集成CustomTkinter组件
- [ ] 实现ECG波形绘制
- [ ] 开发诊断面板功能

### Phase 3: 集成阶段 (2-3天)
- [ ] 连接现有ECG诊断逻辑
- [ ] 实现数据绑定和状态管理
- [ ] 添加错误处理和验证
- [ ] 完成功能测试

### Phase 4: 优化阶段 (1-2天)
- [ ] 性能优化和内存管理
- [ ] 跨平台兼容性测试
- [ ] 用户体验改进
- [ ] 文档更新

总预计时间: 6-10天完成现代化GUI重设计