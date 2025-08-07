"""
Direct fix for the multiply sequence error
Apply this patch to fix the matplotlib figure sizing issue
"""

# This is likely in the ECGPlotWidget or OptimizedECGPlotter class
# The error occurs when matplotlib tries to create a figure with float dimensions

def create_fixed_plotter_import():
    """Create a fixed version of the optimized plotter"""
    fixed_import = """
# In ecg_receiver/gui_tkinter/components/optimized_plotter.py
# Change line around line 20-25 from:
# self.fig = Figure(figsize=(width/100, height/100), dpi=100)
# To:
# self.fig = Figure(figsize=(int(width//100), int(height//100)), dpi=100)

# Or more safely:
width_inches = max(1, int(width // 100))
height_inches = max(1, int(height // 100))
self.fig = Figure(figsize=(width_inches, height_inches), dpi=100)
"""
    return fixed_import

if __name__ == "__main__":
    print("🔧 Type Error Fix for ECG GUI")
    print("=" * 40)
    print("The error 'can't multiply sequence by non-int of type float' is caused by:")
    print("1. Matplotlib figure size calculation using float division")
    print("2. String concatenation with float values")
    print("")
    print("Quick fix:")
    print("Replace figure size calculations with integer values")
    print("")
    print(create_fixed_plotter_import())