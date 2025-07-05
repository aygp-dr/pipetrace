#!/usr/bin/env python3
"""
Example script demonstrating the use of pipetrace.
"""

import time
import random
from pipetrace import trace, logger

@trace
def calculate_something(a, b):
    """Simulate a calculation with some delay."""
    logger.info(f"Calculating with inputs: a={a}, b={b}")
    time.sleep(random.uniform(0.1, 0.5))
    return a * b + random.randint(1, 10)

@trace
def process_data():
    """Process some simulated data with potential errors."""
    logger.info("Starting data processing")
    
    # Simulate some processing steps
    total = 0
    for i in range(5):
        logger.info(f"Processing batch {i+1}")
        value = calculate_something(i, i+1)
        total += value
        
        # Randomly fail sometimes
        if random.random() < 0.2:
            raise ValueError("Random processing error occurred")
    
    return total

@trace
def main():
    """Main function."""
    logger.info("Starting example program")
    
    try:
        result = process_data()
        logger.info(f"Processing completed with result: {result}")
    except Exception as e:
        logger.error(f"Main program caught error: {e}")
    
    logger.info("Example program completed")

if __name__ == "__main__":
    main()
