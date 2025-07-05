#!/usr/bin/env python3
"""
Utility to read from the pipetrace FIFO and display the control flow.
"""

import os
import sys
import time
import signal
import threading

# FIFO configuration
FIFO_PATH = '/tmp/pipetrace_fifo'

def handle_signal(sig, frame):
    """Handle interrupt signal."""
    print("\nExiting FIFO reader...")
    sys.exit(0)

def main():
    """Main function to read from the FIFO."""
    if not os.path.exists(FIFO_PATH):
        print(f"Error: FIFO {FIFO_PATH} does not exist.")
        print("Make sure pipetrace is running first.")
        sys.exit(1)
    
    print(f"Reading from FIFO: {FIFO_PATH}")
    print("Press Ctrl+C to exit")
    
    # Set up signal handler
    signal.signal(signal.SIGINT, handle_signal)
    
    try:
        while True:
            # Open FIFO for reading
            with open(FIFO_PATH, 'r') as fifo:
                for line in fifo:
                    line = line.strip()
                    
                    # Format based on content
                    if line.startswith("ENTER:"):
                        print(f"\033[94m→ {line}\033[0m")  # Blue for entry
                    elif line.startswith("EXIT:"):
                        if "Exception" in line:
                            print(f"\033[91m← {line}\033[0m")  # Red for exception
                        else:
                            print(f"\033[92m← {line}\033[0m")  # Green for success
                    else:
                        print(f"  {line}")  # Plain for other messages
            
            # If FIFO is closed, wait and retry
            time.sleep(0.5)
    except IOError as e:
        print(f"Error reading from FIFO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
