"""
Optimized ECG Plotting with Matplotlib Blitting
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
except ImportError:
    # Fallback for older matplotlib versions
    from matplotlib.backends.backend_tkagg import FigureCanvasTkinter as FigureCanvas
from matplotlib.figure import Figure
from typing import List, Optional
import time

class OptimizedECGPlotter:
    """High-performance ECG plotting with blitting"""
    
    def __init__(self, parent_widget, width=800, height=400):
        self.parent = parent_widget
        self.width = width
        self.height = height
        
        # Create figure with optimal settings
        self.fig = Figure(figsize=(width/100, height/100), dpi=100)
        self.fig.patch.set_facecolor('#0f172a')
        
        # Create subplot
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e293b')
        self.ax.grid(True, alpha=0.3, color='#374151')
        
        # Initialize plot line
        self.line, = self.ax.plot([], [], '#10b981', linewidth=1.5)
        
        # Canvas setup
        self.canvas = FigureCanvas(self.fig, parent_widget)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Performance optimization
        self.background = None
        self.last_update = 0
        self.update_interval = 50  # ms
        
        # Data management
        self.x_data = np.array([])
        self.y_data = np.array([])
        self.max_points = 2000  # Show last 8 seconds at 250Hz
        
    def setup_blitting(self):
        """Setup matplotlib blitting for performance"""
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        
    def update_data(self, new_data: List[float], sample_rate: int = 250):
        """Update plot data with decimation"""
        current_time = time.time() * 1000
        
        # Throttle updates for performance
        if current_time - self.last_update < self.update_interval:
            return
            
        self.last_update = current_time
        
        # Convert to numpy array
        new_data = np.array(new_data, dtype=np.float32)
        
        # Decimate data if too many points (show every 2nd point for performance)
        if len(new_data) > 100:
            new_data = new_data[::2]
        
        # Update data arrays
        new_x = np.linspace(len(self.y_data), len(self.y_data) + len(new_data), len(new_data))
        
        self.x_data = np.append(self.x_data, new_x)
        self.y_data = np.append(self.y_data, new_data)
        
        # Limit data points for performance
        if len(self.y_data) > self.max_points:
            excess = len(self.y_data) - self.max_points
            self.x_data = self.x_data[excess:]
            self.y_data = self.y_data[excess:]
        
        self.render_plot()
    
    def render_plot(self):
        """Render plot using blitting for performance"""
        if len(self.y_data) == 0:
            return
            
        try:
            # Restore background
            if self.background:
                self.canvas.restore_region(self.background)
            
            # Update line data
            self.line.set_data(self.x_data, self.y_data)
            
            # Auto-scale axes efficiently
            if len(self.x_data) > 0:
                self.ax.set_xlim(self.x_data[0], self.x_data[-1])
                
                y_min, y_max = np.min(self.y_data), np.max(self.y_data)
                y_range = y_max - y_min
                if y_range > 0:
                    self.ax.set_ylim(y_min - y_range * 0.1, y_max + y_range * 0.1)
            
            # Draw only the line (fast)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
            
        except Exception as e:
            # Fallback to full redraw
            self.canvas.draw()
    
    def clear_plot(self):
        """Clear all plot data"""
        self.x_data = np.array([])
        self.y_data = np.array([])
        self.line.set_data([], [])
        self.canvas.draw()
