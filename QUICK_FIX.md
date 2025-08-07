# Quick Fix for "Invalid data format" Error

## Your Issue
You were getting errors like:
```
Invalid data format: -7...
Invalid data format: -6...
Invalid data format: -5...
```

## The Problem
Your ESP32 is sending simple numeric values (like `-7`, `-6`, `-5`) instead of the expected CSV format (`DATA,timestamp,ecg_value,...`).

## The Solution ✅
The code has been updated to automatically handle your data format!

## What to Do Now

1. **Copy the updated files** to your Windows system
2. **Run the ECG receiver** as before:
   ```cmd
   python -m ecg_receiver.main
   ```
3. **Connect to COM7** - it should now work!

## Testing (Optional)
Before running the main application, you can test your data format:
```cmd
python analyze_data_format.py
```

This will show you exactly what data your ESP32 is sending and confirm it's working.

## What Changed
- ✅ Now accepts simple numeric values per line
- ✅ Handles negative numbers (like -7, -6, -5)
- ✅ Handles positive numbers (like 1024, 1050)
- ✅ Still supports the original CSV format if you upgrade your ESP32 code later
- ✅ Better error messages and debugging

## Expected Result
Instead of "Invalid data format" errors, you should now see:
- Successful connection to COM7
- ECG waveform displaying your numeric data
- Occasional debug messages like "Received ECG value: -7 (Packet #50)"

Your ESP32 is working fine - it was just a data format compatibility issue that's now fixed!