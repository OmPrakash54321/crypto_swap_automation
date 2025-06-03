import pyautogui
import time
import sys
import os
import platform
from playsound import playsound

# Constants
ITERATIONS = 10
TIMEOUT = 20  # seconds
AMOUNTS = ["1", "1"]  # Alternate these each iteration

# Image file paths
IMG_SWAP_BUTTON = 'swap_button.png'
IMG_SELL_FIELD = 'sell_field.png'
IMG_APPROVE_WALLET = 'approve_wallet.png'
IMG_SWAP_AGAIN = 'swap_again.png'
IMG_LOADING_ICON = 'loading_icon.png'
IMG_ARROW = 'arrow.png'

# Setup PyAutoGUI delays
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def print_cursor_pos():
    x, y = pyautogui.position()
    print(f"Mouse position: ({x}, {y})")

def play_error_sound():
    try:
        playsound('error.mp3')  # Put error.mp3 in same folder
    except:
        print("[WARNING] Could not play error sound.")

def fail_and_exit(message):
    print(f"[ERROR] {message}")
    play_error_sound()
    sys.exit(1)

def wait_for_image(image_path, timeout=TIMEOUT, region=None):
    print(f"Waiting for {image_path} to appear...")
    start = time.time()
    while time.time() - start < timeout:
        print(f'waiting... time {start}')
        location = pyautogui.locateOnScreen(image_path, confidence=0.85, region=region)
        print(f'location {location}')
        if location:
            print(f"Found {image_path}")
            return location
        time.sleep(0.5)
    fail_and_exit(f"Timeout: {image_path} not found")

def click_image(image_path, timeout=TIMEOUT, region=None):
    location = wait_for_image(image_path, timeout, region)
    pyautogui.moveTo(pyautogui.center(location))
    pyautogui.click()

def type_into_field(image_path, text):
    location = wait_for_image(image_path)
    pyautogui.click(pyautogui.center(location))
    # pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(text)

def wait_until_gone(image_path, timeout=TIMEOUT, region=None):
    print(f"Waiting for {image_path} to disappear...")
    start = time.time()
    while time.time() - start < timeout:
        if not pyautogui.locateOnScreen(image_path, confidence=0.85, region=region):
            print(f"{image_path} is gone.")
            return
        time.sleep(0.5)
    fail_and_exit(f"Timeout: {image_path} did not disappear")

def main_with_image_recognition():
    time.sleep(5)
    print("Starting swap automation...")

    # Wait for swap
    if not wait_for_image(IMG_SELL_FIELD, timeout=25):
        fail_and_exit("Sell field not found. Are you on the correct page?")

    for i in range(ITERATIONS):
        print(f"\n--- Swap Iteration {i+1}/{ITERATIONS} ---")

        current_amount = AMOUNTS[i % 2]
        print(f"Using amount: {current_amount}")

        # Input new amount
        type_into_field(IMG_SELL_FIELD, current_amount)

        # If first iteration, click "swap", else click "swap again"
        if i == 0:
            click_image(IMG_SWAP_BUTTON, timeout=25, region=(722, 743, 515, 200))
        else:
            click_image(IMG_SWAP_AGAIN, timeout=25)

        # Click "approve" in wallet pop-up (top-right)
        region_top_right = (1600, 0, 320, 810)
        click_image(IMG_APPROVE_WALLET, timeout=25, region=region_top_right)

        # Confirm transaction completion
        wait_for_image(IMG_SWAP_AGAIN, timeout=25)
        click_image(IMG_SWAP_AGAIN)

        # click the arrow to swap between tokens every alternative iteration
        click_image(IMG_ARROW)

        print(f"Iteration {i+1} complete.")

    print("All swaps completed successfully.")


def main_with_position_click():
    time.sleep(5)
    print("Starting swap automation...")

    # Wait for swap
    if not wait_for_image(IMG_SELL_FIELD, timeout=25):
        fail_and_exit("Sell field not found. Are you on the correct page?")

    for i in range(ITERATIONS):
        print(f"\n--- Swap Iteration {i+1}/{ITERATIONS} ---")

        current_amount = AMOUNTS[i % 2]
        print(f"Using amount: {current_amount}")

        # Input new amount
        type_into_field(IMG_SELL_FIELD, current_amount)

        # With 3 seconds for swap to appear and click it
        time.sleep(5)
        pyautogui.moveTo(pyautogui.center((982, 778, 1, 1)))
        pyautogui.click()

        # Click "approve" in wallet pop-up (top-right)
        time.sleep(5)
        pyautogui.moveTo(pyautogui.center((1805, 653, 1, 1)))
        pyautogui.click()

        # Load screen
        time.sleep(30)

        # Confirm transaction completion
        pyautogui.moveTo(pyautogui.center((991, 898, 1, 1)))
        pyautogui.click()
        time.sleep(3)

        # click the arrow to swap between tokens every alternative iteration
        pyautogui.moveTo(pyautogui.center((994, 608, 1, 1)))
        pyautogui.click()
        time.sleep(3)

        print(f"Iteration {i+1} complete.")

    print("All swaps completed successfully.")


if __name__ == "__main__":
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     print("User interrupted.")
    #     sys.exit(0)
    # except Exception as e:
        # fail_and_exit(f"Unexpected error: {repr(e)}")
    
    main_with_position_click()

    # print_cursor_pos()
        
