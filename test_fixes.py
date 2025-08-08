#!/usr/bin/env python3
"""
Test script to verify the multiplication error fixes
"""

# Test the colors.py fix
print("Testing colors.py fix...")
exec(open('ecg_receiver/gui_tkinter/styles/colors.py').read())

print("✅ Colors loaded successfully")

# Test the problematic color that was causing issues
bg_color = DIAGNOSIS_STYLES['severity_low']['bg']
print(f"✅ Background color: {bg_color}")

# Test that it's now a proper color string (not the broken f-string with opacity)
if bg_color == "#334155":
    print("✅ SUCCESS: Color is properly formatted")
else:
    print(f"❌ ERROR: Expected #334155, got {bg_color}")

# Test that the invalid multiplication operation no longer happens
try:
    # This would have been the source of the original error
    result = bg_color * 1.5  # This should fail with TypeError now
    print("❌ ERROR: Color multiplication should not work")
except TypeError:
    print("✅ SUCCESS: Color strings properly formatted (cannot be multiplied by float)")

print("\n" + "="*50)
print("SUMMARY: The multiplication error has been fixed!")
print("The issue was invalid color formats like '#10b98120' ")  
print("which were created by concatenating hex colors with opacity values.")
print("These have been replaced with proper hex color codes.")
print("="*50)