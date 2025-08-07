"""
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
        
        print("\n📊 Performance Summary")
        print("=" * 30)
        print(f"Runtime: {report['runtime_seconds']:.1f}s")
        print(f"CPU Usage: {report['cpu_percent']:.1f}%") 
        print(f"Memory: {report['memory_mb']}MB")
        print(f"Frame Rate: {report['frame_rate']}fps")
        print(f"Updates: {report['total_updates']}")
        print(f"Avg Update Time: {report['avg_update_time_ms']}ms")
