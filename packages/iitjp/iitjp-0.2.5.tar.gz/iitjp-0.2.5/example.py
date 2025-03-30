"""
Example usage of the IITJP library
"""

import iitjp

# Enable silent mode to avoid audio playback issues
print("Enabling silent mode...")
iitjp.enable_silent_mode(True)

# Use the mam object to interact with the virtual teacher
print("\nRunning greeting:")
iitjp.mam.greetings()

print("\nYou can now use other commands like:")
print("- iitjp.mam.quiz() - Start a quiz")
print("- iitjp.mam.quitquiz() - Quit the current quiz")
print("- iitjp.mam.thanks() - Say thank you and exit")

print("\nEnd of example") 