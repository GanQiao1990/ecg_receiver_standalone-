"""
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
