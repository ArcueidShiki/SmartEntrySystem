from datetime import datetime
import os
import numpy as np
import pyautogui as pag
import cv2
import pytesseract
import subprocess
import time

# Get the bottom_left_position of WhatsApp

script = '''
    tell application "System Events"
        tell process "Chrome"
            set window_pos to get the position of window 1
            set window_size to get the size of window 1
            return {item 1 of window_pos, item 2 of window_pos, item 1 of window_size, item 2 of window_size}
        end tell
    end tell
'''

def get_position_of_the_browser():
    while True:
        window_info = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        output = window_info.stdout.strip()
        if output:
            # print(window_info.stdout.strip()) #This code is for verification
            break
        else:
            print("Your browser is not found.")
        # time.sleep(0.01) 

    x, y, width, height = map(int, window_info.stdout.split(", "))
    return x, y, width, height


def capture_specified_area(word1, word2):
    x, y, width, height = get_position_of_the_browser()

    words_found = {word1: False, word2: False}
    word1_x, word1_y, word2_x, word2_y = None, None, None, None

    while not all(words_found.values()):
        # Check if the position of the browser has changed
        new_x, new_y, new_width, new_height = get_position_of_the_browser()

        # Update position and size if the window has moved or resized
        if (x, y, width, height) != (new_x, new_y, new_width, new_height):
            x, y, width, height = new_x, new_y, new_width, new_height

        # Take a screenshot of the Brave window only
        screenshot = pag.screenshot(region=(x, y, width, height))
        screenshot.save("temp.png")

        # Convert the screenshot to a format that OpenCV can work with
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGBA2BGR)

        # Use pytesseract to detect text in the image
        gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
        data["text"] = [text.lower() for text in data["text"]]

        # Loop through detected text to find both specified words
        for i in range(len(data['text'])):
            if word1 in data['text'][i] and not words_found[word1]:
                (x1, y1, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                word1_x = x1 + x
                word1_y = y1 + y
                words_found[word1] = True
                # print(f"{word1} found at: ({word1_x}, {word1_y})")

            if word2 in data['text'][i] and not words_found[word2]:
                (x1, y1, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                word2_x = x1 + x
                word2_y = y1 + h + y
                words_found[word2] = True
                # print(f"{word2} found at: ({word2_x}, {word2_y})")

        # time.sleep(0.01)  # Increased sleep time for efficiency

    if word1_x is not None and word2_y is not None:
        # Define the area for the screenshot
        area_x = word1_x - 40
        area_y = word1_y - 40  
        area_width = width - (word1_x - x)
        area_height = word2_y - word1_y + 80

        while True:
            try:
                time.sleep(5)
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"static/images/screenshot_{current_time}.png"
                screenshot = pag.screenshot(region=(area_x, area_y, area_width, area_height))
                screenshot.save(screenshot_filename)
                print(f"Screenshot of the specified area saved as {screenshot_filename}.")
                return screenshot_filename

            except ValueError as e:
                print(f"Error taking screenshot: {e}")
    os.remove("temp.png")

