"""
Modern ECG AI Diagnosis GUI - Colors and Themes
Based on medical device design principles with dark theme
"""

# Primary Colors - Medical Blue Theme
PRIMARY_BLUE = "#1e3a8a"      # Deep blue - primary actions
SECONDARY_BLUE = "#3b82f6"    # Standard blue - secondary elements  
LIGHT_BLUE = "#93c5fd"        # Light blue - accents and highlights
ACCENT_BLUE = "#60a5fa"       # Medium blue - hover states

# Background Colors - Dark Professional Theme
BG_DARK = "#0f172a"           # Main dark background
BG_CARD = "#1e293b"           # Card/panel background
BG_LIGHT = "#334155"          # Light background elements
BG_HOVER = "#475569"          # Hover state background

# Text Colors
TEXT_WHITE = "#ffffff"        # Primary text - high contrast
TEXT_LIGHT = "#f1f5f9"        # Secondary text - medium contrast
TEXT_GRAY = "#94a3b8"         # Tertiary text - low contrast  
TEXT_ACCENT = "#fbbf24"       # Accent text - warnings/highlights

# Status Colors - Medical Standards
SUCCESS_GREEN = "#10b981"     # Normal/healthy status
WARNING_YELLOW = "#f59e0b"    # Attention needed
ERROR_RED = "#ef4444"         # Error/problem state
CRITICAL_RED = "#dc2626"      # Critical/emergency state

# ECG Specific Colors
ECG_GRID = "#374151"          # Grid lines
ECG_WAVE = "#10b981"          # ECG waveform - green (medical standard)
ECG_BASELINE = "#6b7280"      # Baseline reference

# Diagnosis Severity Colors
SEVERITY_COLORS = {
    "low": SUCCESS_GREEN,      # Low severity - green
    "moderate": WARNING_YELLOW, # Moderate - yellow  
    "high": ERROR_RED,         # High - red
    "critical": CRITICAL_RED   # Critical - dark red
}

# Button Color Schemes
BUTTON_PRIMARY = {
    "bg": PRIMARY_BLUE,
    "fg": TEXT_WHITE,
    "hover_bg": SECONDARY_BLUE,
    "active_bg": "#1d4ed8",
    "disabled_bg": "#475569",
    "disabled_fg": TEXT_GRAY
}

BUTTON_SECONDARY = {
    "bg": BG_LIGHT,
    "fg": TEXT_WHITE, 
    "hover_bg": BG_HOVER,
    "active_bg": "#1e293b",
    "border": SECONDARY_BLUE
}

BUTTON_SUCCESS = {
    "bg": SUCCESS_GREEN,
    "fg": TEXT_WHITE,
    "hover_bg": "#059669",
    "active_bg": "#047857"
}

BUTTON_WARNING = {
    "bg": WARNING_YELLOW,
    "fg": BG_DARK,
    "hover_bg": "#d97706", 
    "active_bg": "#b45309"
}

BUTTON_DANGER = {
    "bg": ERROR_RED,
    "fg": TEXT_WHITE,
    "hover_bg": "#dc2626",
    "active_bg": "#b91c1c"
}

# Input Field Colors
INPUT_STYLE = {
    "bg": BG_LIGHT,
    "fg": TEXT_WHITE,
    "border": TEXT_GRAY,
    "focus_border": SECONDARY_BLUE,
    "placeholder": TEXT_GRAY,
    "disabled_bg": "#1e293b",
    "disabled_fg": "#64748b"
}

# Card/Panel Colors  
CARD_STYLE = {
    "bg": BG_CARD,
    "border": "#475569",
    "shadow": "rgba(0, 0, 0, 0.25)",
    "header_bg": BG_LIGHT,
    "divider": "#475569"
}

# Progress/Loading Colors
PROGRESS_COLORS = {
    "track_bg": BG_LIGHT,
    "progress_bg": SECONDARY_BLUE,
    "text": TEXT_WHITE
}

# Theme Configuration
DARK_THEME = {
    "name": "dark",
    "primary": PRIMARY_BLUE,
    "secondary": SECONDARY_BLUE, 
    "background": BG_DARK,
    "surface": BG_CARD,
    "text": TEXT_WHITE,
    "text_secondary": TEXT_GRAY
}

# Font Definitions
FONT_FAMILY = "Segoe UI"  # Windows/Cross-platform
FONT_FAMILY_MONO = "Consolas"  # Monospace for data display

FONT_SIZES = {
    "title": 24,      # Main title
    "heading": 18,    # Section headings  
    "subheading": 16, # Subsection headings
    "body": 12,       # Normal text
    "small": 10,      # Small text/captions
    "tiny": 8         # Very small text
}

FONT_WEIGHTS = {
    "light": "light",
    "normal": "normal", 
    "medium": "bold",
    "bold": "bold"
}

# Layout Constants
LAYOUT = {
    "window_width": 1400,
    "window_height": 900,
    "header_height": 80,
    "footer_height": 40,
    "sidebar_width": 560,  # Right panel width
    "main_content_width": 840,  # Left panel width
    
    # Padding and Margins
    "padding_xs": 4,
    "padding_sm": 8,
    "padding_md": 16,
    "padding_lg": 24,
    "padding_xl": 32,
    
    # Border Radius
    "radius_sm": 6,
    "radius_md": 8,
    "radius_lg": 12,
    "radius_xl": 16,
    
    # Shadows
    "shadow_sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
}

# Animation/Transition Settings
ANIMATIONS = {
    "fast": 150,      # Fast transitions (ms)
    "normal": 300,    # Normal transitions (ms)  
    "slow": 500,      # Slow transitions (ms)
    "ease": "ease-in-out"  # Easing function
}

# Icon Definitions (Unicode symbols for now, can be replaced with actual icons)
ICONS = {
    "heart": "🫀",
    "settings": "⚙️", 
    "help": "❓",
    "connect": "🔌",
    "disconnect": "🔌❌", 
    "record": "⏺️",
    "stop": "⏹️",
    "play": "▶️",
    "pause": "⏸️",
    "success": "✅",
    "warning": "⚠️", 
    "error": "❌",
    "info": "ℹ️",
    "refresh": "🔄",
    "download": "⬇️",
    "upload": "⬆️",
    "close": "✖️",
    "minimize": "−",
    "maximize": "□"
}

# ECG Display Settings
ECG_DISPLAY = {
    "grid_color": ECG_GRID,
    "wave_color": ECG_WAVE,
    "wave_width": 2,
    "baseline_color": ECG_BASELINE,
    "background": BG_DARK,
    "grid_alpha": 0.3,
    "update_interval": 50,  # milliseconds
    "buffer_size": 2000,    # data points
    "time_window": 8        # seconds
}

# Status Indicators
STATUS_STYLES = {
    "connected": {
        "color": SUCCESS_GREEN,
        "icon": "●",
        "text": "Connected"
    },
    "disconnected": {
        "color": TEXT_GRAY,
        "icon": "○", 
        "text": "Disconnected"
    },
    "connecting": {
        "color": WARNING_YELLOW,
        "icon": "◐",
        "text": "Connecting..."
    },
    "error": {
        "color": ERROR_RED,
        "icon": "●",
        "text": "Error"
    }
}

# Diagnosis Panel Settings
DIAGNOSIS_STYLES = {
    "severity_low": {
        "bg": f"{SUCCESS_GREEN}20",  # 20% opacity
        "border": SUCCESS_GREEN,
        "text": SUCCESS_GREEN
    },
    "severity_moderate": {
        "bg": f"{WARNING_YELLOW}20",
        "border": WARNING_YELLOW, 
        "text": WARNING_YELLOW
    },
    "severity_high": {
        "bg": f"{ERROR_RED}20",
        "border": ERROR_RED,
        "text": ERROR_RED
    },
    "severity_critical": {
        "bg": f"{CRITICAL_RED}20",
        "border": CRITICAL_RED,
        "text": CRITICAL_RED
    }
}