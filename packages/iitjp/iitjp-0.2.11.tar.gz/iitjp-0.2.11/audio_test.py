"""
Test script for IITJP audio playback with winsound
"""
import iitjp
import time

print("IITJP Audio Test - Testing winsound implementation")
print("=" * 60)

# First test without silent mode
print("1. Testing audio playback with default settings:")
print("   Playing greeting message (should use winsound)...")
iitjp.mam.greetings()

time.sleep(2)  # Wait for a moment

# Now test with silent mode
print("\n2. Testing silent mode (no audio):")
iitjp.enable_silent_mode(True)
print("   Playing farewell message with silent mode enabled...")
iitjp.mam.thanks()

print("\nTest complete! If you heard audio in the first test but not the second, winsound is working correctly.") 