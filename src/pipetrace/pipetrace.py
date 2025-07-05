#!/usr/bin/env python3
"""
Pipetrace - A simple control flow tracing tool using FIFOs for debugging.
"""

import os
import sys
import time
import logging
import inspect
import atexit
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('pipetrace')

# FIFO configuration
FIFO_PATH = '/tmp/pipetrace_fifo'

def create_fifo():
    """Create the debug FIFO if it doesn't exist."""
    if not os.path.exists(FIFO_PATH):
        try:
            os.mkfifo(FIFO_PATH)
            logger.info(f"Created FIFO at {FIFO_PATH}")
        except OSError as e:
            logger.error(f"Failed to create FIFO: {e}")
            sys.exit(1)

def cleanup():
    """Clean up resources on exit."""
    if os.path.exists(FIFO_PATH):
        try:
            os.unlink(FIFO_PATH)
            logger.info(f"Removed FIFO at {FIFO_PATH}")
        except OSError as e:
            logger.error(f"Failed to remove FIFO: {e}")

def write_to_fifo(message):
    """Write a message to the FIFO."""
    try:
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write(f"{message}\n")
            fifo.flush()
    except IOError as e:
        logger.error(f"Failed to write to FIFO: {e}")

def trace(func):
    """Decorator to trace function entry and exit."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_info = inspect.getframeinfo(caller_frame)
        
        # Entry message
        entry_msg = f"ENTER: {func.__name__} from {caller_info.function} ({caller_info.filename}:{caller_info.lineno})"
        logger.info(entry_msg)
        write_to_fifo(entry_msg)
        
        # Call the function
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            # Exit message (success)
            elapsed = time.time() - start_time
            exit_msg = f"EXIT: {func.__name__} (elapsed: {elapsed:.4f}s) - Success"
            logger.info(exit_msg)
            write_to_fifo(exit_msg)
            return result
        except Exception as e:
            # Exit message (exception)
            elapsed = time.time() - start_time
            exit_msg = f"EXIT: {func.__name__} (elapsed: {elapsed:.4f}s) - Exception: {type(e).__name__}: {str(e)}"
            logger.error(exit_msg)
            write_to_fifo(exit_msg)
            raise
    
    return wrapper

# Initialize on import
create_fifo()
atexit.register(cleanup)

if __name__ == "__main__":
    logger.info("Pipetrace module is ready.")
    logger.info(f"Use 'cat {FIFO_PATH}' in another terminal to view traces.")
