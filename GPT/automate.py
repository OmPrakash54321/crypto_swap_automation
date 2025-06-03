import pyautogui
import time
import logging
import sys
import os

# Config
CONFIDENCE = 0.9
SWAP_AMOUNT = "0.3"
TIMEOUT = 60  # seconds

# Paths to images (ensure these are in the script's directory)
IMG_SWAP_BTN = "swap_button.png"
IMG_SELL_FIELD = "sell_field.png"
IMG_APPROVE = "approve_wallet.png"
IMG_SWAP_AGAIN = "swap_again.png"
IMG_LOADING = "loading_icon.png"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def wait_for(image, timeout=TIMEOUT):
    start = time.time()
    while time.time() - start < timeout:
        loc = pyautogui.locateCenterOnScreen(image, confidence=CONFIDENCE)
        if loc:
            return loc
        time.sleep(0.5)
    raise TimeoutError(f"Timeout waiting for: {image}")

def click_image(image, description):
    logging.info(f"Waiting for {description}...")
    loc = wait_for(image)
    logging.info(f"Clicking {description} at {loc}")
    pyautogui.moveTo(loc)
    pyautogui.click()

def type_swap_amount():
    logging.info("Typing swap amount...")
    loc = wait_for(IMG_SELL_FIELD)
    pyautogui.click(loc)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(SWAP_AMOUNT)

def wait_for_loading_to_finish():
    logging.info("Waiting for transaction to complete...")
    while pyautogui.locateOnScreen(IMG_LOADING, confidence=CONFIDENCE):
        time.sleep(1)
    logging.info("Transaction completed.")

def run_cycle():
    type_swap_amount()
    click_image(IMG_SWAP_BTN, "Swap button")
    click_image(IMG_APPROVE, "Approve in wallet")
    wait_for_loading_to_finish()
    click_image(IMG_SWAP_AGAIN, "Swap Again button")

def main():
    try:
        while True:
            run_cycle()
            time.sleep(2)  # slight pause before next cycle
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

