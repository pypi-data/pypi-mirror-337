"""
Test script for IITJP command-line interface
"""
import subprocess
import time
import sys

print("IITJP Command-Line Interface Test")
print("=" * 60)

# Get the Python executable path
python_executable = sys.executable

# First test the greetings command
print("1. Testing 'iitjp greetings' command:")
try:
    # Use subprocess to run the command
    subprocess.run([python_executable, "-m", "iitjp", "greetings"], 
                  check=True, timeout=10)
    print("   ✓ Greetings command executed successfully")
except Exception as e:
    print(f"   ✗ Error running greetings command: {e}")

time.sleep(1)  # Wait for a moment

# Now test with silent mode
print("\n2. Testing silent mode with 'iitjp --silent thanks' command:")
try:
    # Use subprocess to run the command with silent flag
    subprocess.run([python_executable, "-m", "iitjp", "--silent", "thanks"], 
                  check=True, timeout=10)
    print("   ✓ Thanks command with silent mode executed successfully")
except Exception as e:
    print(f"   ✗ Error running thanks command: {e}")

print("\n3. Testing 'iitjp version' command:")
try:
    # Use subprocess to run the version command
    result = subprocess.run([python_executable, "-m", "iitjp", "version"], 
                           check=True, timeout=5, capture_output=True, text=True)
    print(f"   ✓ Version command output: {result.stdout.strip()}")
except Exception as e:
    print(f"   ✗ Error running version command: {e}")

print("\nCommand-line interface test complete!") 