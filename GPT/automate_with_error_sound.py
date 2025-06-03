import pyautogui
import time
import sys
import os
import platform

# Use appropriate sound lib based on platform
if platform.system() == 'Windows':
    import winsound
    def play_error_sound():
        winsound.MessageBeep(winsound.MB_ICONHAND)
else:
    from playsound import playsound
    def play_error_sound():
        playsound('error.mp3')  # Add your own error.mp3 for non-Windows

# Setup PyAutoGUI delays
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

# Constants
ITERATIONS = 10
TIMEOUT = 20  # seconds

# Image file paths
IMG_SWAP_BUTTON = 'swap_button.png'
IMG_SELL_FIELD = 'sell_field.png'
IMG_APPROVE_WALLET = 'approve_wallet.png'
IMG_SWAP_AGAIN = 'swap_again.png'
IMG_LOADING_ICON = 'loading_icon.png'

def fail_and_exit(message):
    print(f"[ERROR] {message}")
    play_error_sound()
    sys.exit(1)

def wait_for_image(image_path, timeout=TIMEOUT, region=None):
    print(f"Waiting for {image_path} to appear...")
    start = time.time()
    while time.time() - start < timeout:
        location = pyautogui.locateOnScreen(image_path, confidence=0.85, region=region)
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
    pyautogui.hotkey('ctrl', 'a')
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

def main():
    print("Starting swap automation...")

    # Step 1: Check swap page
    if not pyautogui.locateOnScreen(IMG_SWAP_BUTTON, confidence=0.85):
        fail_and_exit("Swap button not found. Are you on the correct page?")

    for i in range(ITERATIONS):
        print(f"\n--- Swap Iteration {i+1}/{ITERATIONS} ---")

        # Step 2: Input amount
        type_into_field(IMG_SELL_FIELD, "0.0001")

        # Step 3: Click swap
        click_image(IMG_SWAP_BUTTON)

        # Step 4: Wait and approve wallet in top-right
        region_top_right = (1000, 0, 280, 400)
        click_image(IMG_APPROVE_WALLET, region=region_top_right)

        # Step 5: Wait for loading to disappear
        wait_until_gone(IMG_LOADING_ICON, timeout=25)

        # Step 6: Confirm "Swap Again" appears
        wait_for_image(IMG_SWAP_AGAIN, timeout=25)

        print(f"Iteration {i+1} complete.")

    print("All swaps completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User interrupted.")
        sys.exit(0)
    except Exception as e:
        fail_and_exit(f"Unexpected error: {str(e)}")

