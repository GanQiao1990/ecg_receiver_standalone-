"""
Modern ECG AI Diagnosis GUI - Custom Components
CustomTkinter-based modern UI components
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
except ImportError:
    # Fallback for older matplotlib versions
    from matplotlib.backends.backend_tkagg import FigureCanvasTkinter as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from typing import Callable, Optional, List, Dict, Any
import threading
import time

from ..styles.colors import *

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernCard(ctk.CTkFrame):
    """Modern card component with shadow effect"""
    
    def __init__(self, parent, title: str = "", **kwargs):
        # Default card styling
        card_kwargs = {
            "fg_color": BG_CARD,
            "border_width": 1,
            "border_color": CARD_STYLE["border"],
            "corner_radius": LAYOUT["radius_lg"]
        }
        card_kwargs.update(kwargs)
        
        super().__init__(parent, **card_kwargs)
        
        self.title = title
        self.create_layout()
    
    def create_layout(self):
        """Create card layout with optional title"""
        if self.title:
            # Title bar
            self.title_frame = ctk.CTkFrame(
                self,
                fg_color=BG_LIGHT,
                height=40,
                corner_radius=(LAYOUT["radius_lg"], LAYOUT["radius_lg"], 0, 0)
            )
            self.title_frame.pack(fill="x", padx=0, pady=(0, 1))
            self.title_frame.pack_propagate(False)
            
            # Title label
            self.title_label = ctk.CTkLabel(
                self.title_frame,
                text=self.title,
                font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["subheading"], weight="bold"),
                text_color=TEXT_WHITE
            )
            self.title_label.pack(side="left", padx=LAYOUT["padding_md"], pady=LAYOUT["padding_sm"])
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=LAYOUT["padding_md"], pady=LAYOUT["padding_md"])
    
    def get_content_frame(self):
        """Get the content frame for adding widgets"""
        return self.content_frame

class ECGPlotWidget(ctk.CTkFrame):
    """Modern ECG plotting widget with real-time updates"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_DARK, corner_radius=LAYOUT["radius_md"], **kwargs)
        
        self.data_buffer = []
        self.time_buffer = []
        self.max_points = ECG_DISPLAY["buffer_size"]
        self.time_window = ECG_DISPLAY["time_window"]
        self.update_interval = ECG_DISPLAY["update_interval"]
        
        self.setup_plot()
        self.start_animation()
    
    def setup_plot(self):
        """Setup matplotlib plot with medical ECG styling"""
        # Create figure with dark background
        plt.style.use('dark_background')
        self.figure = Figure(figsize=(10, 4), dpi=100)
        self.figure.patch.set_facecolor(BG_DARK)
        
        # Create subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(BG_DARK)
        
        # Configure ECG-style grid
        self.ax.grid(True, color=ECG_GRID, alpha=0.3, linewidth=0.5)
        self.ax.set_xlabel("Time (seconds)", color=TEXT_GRAY, fontsize=10)
        self.ax.set_ylabel("Amplitude (μV)", color=TEXT_GRAY, fontsize=10)
        
        # Configure axes
        self.ax.spines['bottom'].set_color(TEXT_GRAY)
        self.ax.spines['top'].set_color(TEXT_GRAY)
        self.ax.spines['right'].set_color(TEXT_GRAY)
        self.ax.spines['left'].set_color(TEXT_GRAY)
        self.ax.tick_params(colors=TEXT_GRAY, which='both')
        
        # Initial empty line
        self.line, = self.ax.plot([], [], color=ECG_WAVE, linewidth=2, antialiased=True)
        
        # Set initial limits
        self.ax.set_xlim(0, self.time_window)
        self.ax.set_ylim(-200, 200)
        
        # Create canvas
        self.canvas = FigureCanvas(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tight layout
        self.figure.tight_layout()
    
    def add_data_point(self, value: float):
        """Add new ECG data point"""
        current_time = time.time()
        
        # Add to buffers
        self.data_buffer.append(value)
        self.time_buffer.append(current_time)
        
        # Maintain buffer size
        if len(self.data_buffer) > self.max_points:
            self.data_buffer.pop(0)
            self.time_buffer.pop(0)
    
    def update_plot(self):
        """Update the plot with new data"""
        if not self.data_buffer:
            return
        
        # Convert to relative time (last N seconds)
        if self.time_buffer:
            current_time = self.time_buffer[-1]
            relative_times = [(t - current_time) + self.time_window for t in self.time_buffer]
            
            # Filter data within time window
            valid_indices = [i for i, t in enumerate(relative_times) if t >= 0]
            if valid_indices:
                plot_times = [relative_times[i] for i in valid_indices]
                plot_data = [self.data_buffer[i] for i in valid_indices]
                
                # Update line data
                self.line.set_data(plot_times, plot_data)
                
                # Auto-scale Y axis based on data
                if plot_data:
                    y_min, y_max = min(plot_data), max(plot_data)
                    y_range = y_max - y_min
                    margin = y_range * 0.1 if y_range > 0 else 100
                    self.ax.set_ylim(y_min - margin, y_max + margin)
        
        # Redraw
        self.canvas.draw_idle()
    
    def start_animation(self):
        """Start real-time plot updates"""
        def animate():
            while True:
                try:
                    self.after(0, self.update_plot)
                    time.sleep(self.update_interval / 1000.0)
                except:
                    break
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def clear_data(self):
        """Clear all data buffers"""
        self.data_buffer.clear()
        self.time_buffer.clear()
        self.line.set_data([], [])
        self.canvas.draw_idle()

class StatusIndicator(ctk.CTkFrame):
    """Modern status indicator with color-coded states"""
    
    def __init__(self, parent, status: str = "disconnected", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.status = status
        self.create_layout()
        self.update_status(status)
    
    def create_layout(self):
        """Create status indicator layout"""
        # Status dot
        self.status_dot = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=16),
            width=20
        )
        self.status_dot.pack(side="left", padx=(0, 5))
        
        # Status text
        self.status_text = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["small"], weight="bold")
        )
        self.status_text.pack(side="left")
    
    def update_status(self, status: str):
        """Update status indicator"""
        self.status = status
        style = STATUS_STYLES.get(status, STATUS_STYLES["disconnected"])
        
        self.status_dot.configure(text_color=style["color"])
        self.status_text.configure(text=style["text"], text_color=style["color"])

class ModernButton(ctk.CTkButton):
    """Enhanced button with hover effects and icons"""
    
    def __init__(self, parent, style: str = "primary", icon: str = None, **kwargs):
        # Get button style
        if style == "primary":
            button_style = BUTTON_PRIMARY
        elif style == "secondary":
            button_style = BUTTON_SECONDARY
        elif style == "success":
            button_style = BUTTON_SUCCESS
        elif style == "warning":
            button_style = BUTTON_WARNING
        elif style == "danger":
            button_style = BUTTON_DANGER
        else:
            button_style = BUTTON_PRIMARY
        
        # Apply styling
        button_kwargs = {
            "fg_color": button_style["bg"],
            "hover_color": button_style["hover_bg"],
            "text_color": button_style["fg"],
            "font": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"], weight="bold"),
            "corner_radius": LAYOUT["radius_md"],
            "height": 36
        }
        
        # Add border for secondary buttons
        if style == "secondary":
            button_kwargs["border_width"] = 1
            button_kwargs["border_color"] = button_style["border"]
        
        button_kwargs.update(kwargs)
        
        # Add icon to text if provided
        text = kwargs.get("text", "")
        if icon and icon in ICONS:
            text = f"{ICONS[icon]} {text}"
            button_kwargs["text"] = text
        
        super().__init__(parent, **button_kwargs)

class DiagnosisResultCard(ModernCard):
    """Specialized card for displaying diagnosis results"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Diagnosis Results", **kwargs)
        self.setup_content()
    
    def setup_content(self):
        """Setup diagnosis result display"""
        content = self.get_content_frame()
        
        # Diagnosis text area
        self.diagnosis_text = ctk.CTkTextbox(
            content,
            font=ctk.CTkFont(family=FONT_FAMILY_MONO, size=FONT_SIZES["small"]),
            fg_color=BG_DARK,
            text_color=TEXT_WHITE,
            height=200
        )
        self.diagnosis_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Clear button
        self.clear_btn = ModernButton(
            content,
            text="Clear Results",
            style="secondary", 
            height=32,
            command=self.clear_results
        )
        self.clear_btn.pack(side="right")
    
    def update_diagnosis(self, diagnosis: Dict[str, Any]):
        """Update diagnosis display"""
        self.diagnosis_text.delete("1.0", "end")
        
        # Format diagnosis text
        diagnosis_text = self.format_diagnosis(diagnosis)
        self.diagnosis_text.insert("1.0", diagnosis_text)
        
        # Color code based on severity
        severity = diagnosis.get("severity", "unknown").lower()
        if severity in SEVERITY_COLORS:
            color = SEVERITY_COLORS[severity]
            self.diagnosis_text.configure(text_color=color)
    
    def format_diagnosis(self, diagnosis: Dict[str, Any]) -> str:
        """Format diagnosis for display"""
        lines = []
        lines.append("=== ECG DIAGNOSIS REPORT ===")
        lines.append(f"Timestamp: {diagnosis.get('timestamp', 'Unknown')}")
        lines.append("")
        lines.append(f"PRIMARY DIAGNOSIS: {diagnosis.get('primary_diagnosis', 'Unknown')}")
        lines.append(f"SEVERITY: {diagnosis.get('severity', 'unknown').upper()}")
        lines.append(f"CONFIDENCE: {diagnosis.get('confidence', 0):.1%}")
        lines.append("")
        
        # Add other diagnosis details
        if diagnosis.get('key_findings'):
            lines.append("KEY FINDINGS:")
            for finding in diagnosis['key_findings']:
                lines.append(f"• {finding}")
            lines.append("")
        
        if diagnosis.get('recommendations'):
            lines.append("RECOMMENDATIONS:")
            recommendations = diagnosis['recommendations']
            if recommendations.get('immediate_actions'):
                lines.append("Immediate Actions:")
                for action in recommendations['immediate_actions']:
                    lines.append(f"• {action}")
                lines.append("")
        
        return "\n".join(lines)
    
    def clear_results(self):
        """Clear diagnosis results"""
        self.diagnosis_text.delete("1.0", "end")

class ProgressIndicator(ctk.CTkFrame):
    """Modern progress indicator with status text"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.create_layout()
        self.hide()
    
    def create_layout(self):
        """Create progress indicator layout"""
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            progress_color=SECONDARY_BLUE,
            fg_color=BG_LIGHT,
            height=8
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))
        
        # Status text
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["small"]),
            text_color=TEXT_GRAY
        )
        self.status_label.pack()
    
    def show_progress(self, progress: float, text: str = ""):
        """Show progress with optional text"""
        self.pack(fill="x", padx=LAYOUT["padding_md"], pady=LAYOUT["padding_sm"])
        self.progress_bar.set(progress)
        self.status_label.configure(text=text)
    
    def hide(self):
        """Hide progress indicator"""
        self.pack_forget()

class ModernTabView(ctk.CTkTabview):
    """Enhanced tabview with modern styling"""
    
    def __init__(self, parent, **kwargs):
        tab_kwargs = {
            "fg_color": BG_CARD,
            "segmented_button_fg_color": BG_LIGHT,
            "segmented_button_selected_color": SECONDARY_BLUE,
            "segmented_button_selected_hover_color": PRIMARY_BLUE,
            "text_color": TEXT_WHITE
        }
        tab_kwargs.update(kwargs)
        
        super().__init__(parent, **tab_kwargs)