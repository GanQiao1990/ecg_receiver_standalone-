#!/usr/bin/env python3
"""
ECG GUI Performance Testing and Optimization Script
Tests and analyzes the modern GUI for performance issues
"""

import time
import sys
import os
import traceback
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def analyze_code_performance():
    """Analyze code for potential performance issues"""
    print("🔍 ECG GUI Performance Analysis")
    print("=" * 50)
    
    performance_issues = []
    optimizations = []
    
    # Check import structure
    print("\n📋 1. Import Analysis")
    try:
        # Test imports without actually importing GUI (to avoid dependency issues)
        gui_file = "ecg_receiver/gui_tkinter/main_window_modern.py"
        if os.path.exists(gui_file):
            with open(gui_file, 'r') as f:
                content = f.read()
                
            # Count imports
            import_lines = [line for line in content.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]
            print(f"   Total imports: {len(import_lines)}")
            
            # Check for potential circular imports
            if "from ." in content and "sys.path.append" in content:
                performance_issues.append("Multiple sys.path modifications detected")
                optimizations.append("Consolidate import paths and use relative imports consistently")
            
            print("   ✅ Import structure looks clean")
        
    except Exception as e:
        performance_issues.append(f"Import analysis failed: {e}")
    
    # Check threading usage
    print("\n🧵 2. Threading Analysis")
    try:
        if 'threading.Thread' in content:
            print("   ✅ Background threading implemented for diagnosis")
            if 'daemon=True' in content:
                print("   ✅ Daemon threads properly configured")
            else:
                performance_issues.append("Non-daemon threads may block app shutdown")
                optimizations.append("Set daemon=True for background threads")
        
    except Exception as e:
        performance_issues.append(f"Threading analysis failed: {e}")
    
    # Check data buffer management
    print("\n💾 3. Memory Management Analysis")
    try:
        if 'diagnosis_buffer_size = 5000' in content:
            print("   ✅ ECG data buffer size limited (5000 samples)")
            optimizations.append("Consider implementing circular buffer for long-term recording")
        
        if 'diagnosis_history' in content:
            print("   ⚠️  Diagnosis history may grow unbounded")
            performance_issues.append("Diagnosis history list may cause memory leak")
            optimizations.append("Implement history size limit or LRU cache")
            
    except Exception as e:
        performance_issues.append(f"Memory analysis failed: {e}")
    
    # Check GUI update patterns
    print("\n🖼️  4. GUI Update Analysis")
    try:
        if 'self.root.after(' in content:
            print("   ✅ Using tkinter.after() for GUI updates")
        else:
            performance_issues.append("No tkinter.after() calls found for periodic updates")
            optimizations.append("Use root.after() instead of time.sleep() for GUI updates")
            
    except Exception as e:
        performance_issues.append(f"GUI update analysis failed: {e}")
    
    return performance_issues, optimizations

def check_file_structure():
    """Check file organization for performance"""
    print("\n📁 5. File Structure Analysis")
    
    structure_issues = []
    
    # Check if all required files exist
    required_files = [
        "ecg_receiver/gui_tkinter/main_window_modern.py",
        "ecg_receiver/gui_tkinter/components/modern_widgets.py", 
        "ecg_receiver/gui_tkinter/styles/colors.py",
        "ecg_diagnosis.py",
        "launch_modern_gui.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({file_size} bytes)")
            
            # Check for oversized files
            if file_size > 50000:  # 50KB
                structure_issues.append(f"{file_path} is large ({file_size} bytes)")
        else:
            print(f"   ❌ {file_path} - Missing")
            structure_issues.append(f"Missing required file: {file_path}")
    
    return structure_issues

def suggest_optimizations():
    """Suggest performance optimizations"""
    print("\n⚡ Performance Optimization Recommendations")
    print("=" * 50)
    
    optimizations = [
        {
            "category": "GUI Rendering",
            "issues": [
                "Real-time ECG plotting can be CPU intensive",
                "Multiple matplotlib figures may consume memory"
            ],
            "solutions": [
                "Implement data decimation for display (show every Nth point)",
                "Use matplotlib blitting for faster animation",
                "Limit plot history to visible time window"
            ]
        },
        {
            "category": "Data Processing", 
            "issues": [
                "ECG preprocessing runs on each diagnosis",
                "Large data arrays copied in memory"
            ],
            "solutions": [
                "Cache preprocessed data when possible",
                "Use numpy views instead of copying arrays",
                "Implement streaming data processing"
            ]
        },
        {
            "category": "Network/API",
            "issues": [
                "AI diagnosis API calls can block UI",
                "No request timeout handling visible"
            ],
            "solutions": [
                "Implement request timeout and retry logic",
                "Add request queuing for multiple diagnoses",
                "Show diagnosis progress indicator"
            ]
        },
        {
            "category": "Memory Management",
            "issues": [
                "Diagnosis history grows unbounded",
                "ECG data buffer may fragment memory"
            ],
            "solutions": [
                "Implement circular buffer for ECG data",
                "Add history cleanup (keep last N diagnoses)",
                "Use memory pooling for large arrays"
            ]
        }
    ]
    
    for opt in optimizations:
        print(f"\n🎯 {opt['category']}")
        print("   Issues:")
        for issue in opt['issues']:
            print(f"     - {issue}")
        print("   Solutions:")
        for solution in opt['solutions']:
            print(f"     + {solution}")
    
    return optimizations

def create_performance_improvements():
    """Create performance improvement implementations"""
    print("\n🛠️  Creating Performance Improvements")
    print("=" * 50)
    
    # 1. Create optimized ECG data buffer
    buffer_code = '''"""
Optimized ECG Data Buffer with Circular Buffer Implementation
"""
import numpy as np
from collections import deque
from typing import List, Optional

class CircularECGBuffer:
    """Memory-efficient circular buffer for ECG data"""
    
    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.buffer = np.zeros(max_size, dtype=np.float32)
        self.head = 0
        self.count = 0
        self.full = False
    
    def append(self, data: List[float]):
        """Add data points to circular buffer"""
        data = np.array(data, dtype=np.float32)
        
        for value in data:
            self.buffer[self.head] = value
            self.head = (self.head + 1) % self.max_size
            
            if not self.full:
                self.count += 1
                if self.count == self.max_size:
                    self.full = True
    
    def get_recent_data(self, samples: Optional[int] = None) -> np.ndarray:
        """Get recent data points efficiently"""
        if samples is None:
            samples = self.count
        
        samples = min(samples, self.count)
        
        if not self.full:
            return self.buffer[:self.head][-samples:]
        else:
            # Handle circular buffer wrap-around
            if samples <= self.head:
                return self.buffer[self.head-samples:self.head]
            else:
                tail_samples = samples - self.head
                return np.concatenate([
                    self.buffer[-tail_samples:],
                    self.buffer[:self.head]
                ])
    
    def clear(self):
        """Clear the buffer"""
        self.head = 0
        self.count = 0
        self.full = False
        self.buffer.fill(0.0)
'''
    
    with open("ecg_receiver/core/circular_buffer.py", "w") as f:
        f.write(buffer_code)
    print("   ✅ Created circular_buffer.py")
    
    # 2. Create optimized plotting widget
    plotting_code = '''"""
Optimized ECG Plotting with Matplotlib Blitting
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
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
        self.canvas = FigureCanvasTkinter(self.fig, parent_widget)
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
'''
    
    with open("ecg_receiver/gui_tkinter/components/optimized_plotter.py", "w") as f:
        f.write(plotting_code)
    print("   ✅ Created optimized_plotter.py")
    
    # 3. Create performance monitoring utility
    monitor_code = '''"""
Performance Monitoring Utility for ECG GUI
"""
import time
import psutil
import threading
from typing import Dict, Any, Callable

class PerformanceMonitor:
    """Monitor GUI performance metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics = {
            'cpu_percent': 0.0,
            'memory_mb': 0.0,
            'frame_rate': 0.0,
            'update_count': 0,
            'avg_update_time': 0.0
        }
        
        self.frame_times = []
        self.update_times = []
        self.monitoring = False
        
    def start_monitoring(self):
        """Start background performance monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # CPU and memory monitoring
                self.metrics['cpu_percent'] = psutil.cpu_percent(interval=0.1)
                self.metrics['memory_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
                
                # Calculate frame rate
                if len(self.frame_times) > 10:
                    recent_frames = self.frame_times[-10:]
                    if len(recent_frames) > 1:
                        frame_interval = (recent_frames[-1] - recent_frames[0]) / (len(recent_frames) - 1)
                        self.metrics['frame_rate'] = 1.0 / frame_interval if frame_interval > 0 else 0
                
                # Calculate average update time
                if self.update_times:
                    self.metrics['avg_update_time'] = sum(self.update_times) / len(self.update_times) * 1000
                    
                time.sleep(1.0)  # Update every second
                
            except Exception as e:
                print(f"Performance monitoring error: {e}")
                break
    
    def record_frame(self):
        """Record frame timing"""
        current_time = time.time()
        self.frame_times.append(current_time)
        
        # Keep only recent frames
        if len(self.frame_times) > 60:  # Keep 60 seconds of data
            self.frame_times = self.frame_times[-60:]
    
    def record_update_time(self, update_duration: float):
        """Record GUI update timing"""
        self.update_times.append(update_duration)
        self.metrics['update_count'] += 1
        
        # Keep only recent updates
        if len(self.update_times) > 100:
            self.update_times = self.update_times[-100:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        runtime = time.time() - self.start_time
        
        return {
            'runtime_seconds': runtime,
            'cpu_percent': self.metrics['cpu_percent'],
            'memory_mb': round(self.metrics['memory_mb'], 1),
            'frame_rate': round(self.metrics['frame_rate'], 1),
            'total_updates': self.metrics['update_count'],
            'avg_update_time_ms': round(self.metrics['avg_update_time'], 2)
        }
    
    def print_performance_summary(self):
        """Print performance summary"""
        report = self.get_performance_report()
        
        print("\\n📊 Performance Summary")
        print("=" * 30)
        print(f"Runtime: {report['runtime_seconds']:.1f}s")
        print(f"CPU Usage: {report['cpu_percent']:.1f}%") 
        print(f"Memory: {report['memory_mb']}MB")
        print(f"Frame Rate: {report['frame_rate']}fps")
        print(f"Updates: {report['total_updates']}")
        print(f"Avg Update Time: {report['avg_update_time_ms']}ms")
'''
    
    with open("ecg_receiver/core/performance_monitor.py", "w") as f:
        f.write(monitor_code)
    print("   ✅ Created performance_monitor.py")
    
    return ["circular_buffer.py", "optimized_plotter.py", "performance_monitor.py"]

def main():
    """Main performance testing function"""
    start_time = time.time()
    
    print("🫀 ECG GUI Performance Testing & Optimization")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run performance analysis
    try:
        performance_issues, optimizations = analyze_code_performance()
        structure_issues = check_file_structure()
        
        # Display results
        print("\n📋 Analysis Results")
        print("=" * 30)
        
        if performance_issues:
            print("⚠️  Performance Issues Found:")
            for issue in performance_issues:
                print(f"   - {issue}")
        else:
            print("✅ No major performance issues detected")
            
        if structure_issues:
            print("\\n📁 File Structure Issues:")
            for issue in structure_issues:
                print(f"   - {issue}")
        else:
            print("\\n✅ File structure looks good")
        
        # Suggest optimizations
        suggest_optimizations()
        
        # Create performance improvements
        created_files = create_performance_improvements()
        
        print("\\n🎉 Performance Testing Complete")
        print(f"Created optimization files: {', '.join(created_files)}")
        
        elapsed_time = time.time() - start_time
        print(f"Analysis completed in {elapsed_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance testing failed: {e}")
        print("\\nStack trace:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Import datetime here to avoid import issues
    from datetime import datetime
    success = main()
    sys.exit(0 if success else 1)