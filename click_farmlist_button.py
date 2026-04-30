"""
Script to click the 'Start All Farmlist' button in Travian using image recognition.
Requires: pyautogui, opencv-python
"""

import pyautogui
import time
import os
import random
from pathlib import Path
import traceback

# Disable pyautogui's failsafe (move mouse to corner to abort)
# Uncomment if you want this safety feature
# pyautogui.FAILSAFE = True


def move_mouse_smoothly(target_x, target_y):
    """Move the pointer to a target using a short curved path."""
    start_x, start_y = pyautogui.position()
    distance = max(abs(target_x - start_x), abs(target_y - start_y))

    # Use a midpoint that bends the path slightly like a human mouse gesture.
    curve_offset = max(12, min(60, distance // 10))
    mid_x = (start_x + target_x) / 2 + random.randint(-curve_offset, curve_offset)
    mid_y = (start_y + target_y) / 2 + random.randint(-curve_offset, curve_offset)

    first_duration = random.uniform(0.08, 0.18)
    second_duration = random.uniform(0.08, 0.18)

    pyautogui.moveTo(mid_x, mid_y, duration=first_duration, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(target_x, target_y, duration=second_duration, tween=pyautogui.easeInOutQuad)

def find_and_click_button(image_path, confidence=0.8, clicks=1, interval=0.5):
    """
    Find and click on the button image.
    
    Args:
        image_path (str): Path to the button image file
        confidence (float): Confidence level for image matching (0-1)
        clicks (int): Number of clicks to perform
        interval (float): Interval between clicks in seconds
    
    Returns:
        bool: True if button was found and clicked, False otherwise
    """
    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return False
    
    print(f"Looking for button image: {image_path}")
    
    try:
        # Locate the image on screen
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        
        if location is None:
            print("Button not found on screen. Make sure:")
            print("  - The Travian window is visible")
            print("  - The image matches the current screen state")
            print("  - Adjust the confidence parameter if needed")
            return False
        
        # Get the center of the located image
        button_x, button_y = pyautogui.center(location)
        print(f"Button found at coordinates: ({button_x}, {button_y})")
        
        # Click the button
        for i in range(clicks):
            # Add small random offset to simulate human behavior
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            click_x = button_x + offset_x
            click_y = button_y + offset_y

            move_mouse_smoothly(click_x, click_y)
            
            print(f"Clicking button (click {i+1}/{clicks}) at ({click_x}, {click_y})...")
            pyautogui.click(click_x, click_y)
            
            if i < clicks - 1:  # Add interval between multiple clicks
                time.sleep(interval)
        
        print("Done!")
        return True
        
    except Exception:
        # Print full traceback so callers see the cause in logs
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = Path(__file__).parent
    button_image = script_dir / "start_all_farmlist_button.png"
    
    # Add a small delay to give you time to activate the Travian window
    print("Starting in 3 seconds... Make sure the Travian window is active!")
    time.sleep(3)
    
    # Click the button with a top-level guard to print tracebacks for unexpected errors
    try:
        find_and_click_button(str(button_image), confidence=0.8)
    except Exception:
        traceback.print_exc()
        raise
