import os
import time
import pynput
import pyautogui
import pyperclip
import logging
from pynput.keyboard import Key, Controller
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log script started
logging.info("Script started")

# Retrieve environment variables
PY_CORRECTOR_KEY_COMB_FIX_TEXT = os.getenv('PY_CORRECTOR_KEY_COMB_FIX_TEXT')
PY_CORRECTOR_KEY_COMB_FIX_LINE = os.getenv('PY_CORRECTOR_KEY_COMB_FIX_LINE')
PY_CORRECTOR_AI_ADDRESS = os.getenv('PY_CORRECTOR_AI_ADDRESS')
PY_CORRECTOR_API_KEY = os.getenv('PY_CORRECTOR_API_KEY')
PY_CORRECTOR_AI_RULE = os.getenv('PY_CORRECTOR_AI_RULE')

# Initialize OpenAI client and keyboard controller
client = OpenAI(base_url=PY_CORRECTOR_AI_ADDRESS, api_key=PY_CORRECTOR_API_KEY)
keyboard = Controller()

# Define function to make API call
def make_api_call(text):
    try:
        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "user", "content": f"{PY_CORRECTOR_AI_RULE}:{text}"}
            ],
            temperature=0.7,
        )
        final = completion.choices[0].message.content
        if final is not None:
            logging.info(f"Final text: {final}")
            pyperclip.copy(final)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Define function to fix text
def fix_text():
    logging.info("Starting to inspect text")
    try:
        pyperclip.copy('')    # empty the clipboard for this one
        keyboard.press(Key.ctrl)
        keyboard.press('a')
        keyboard.release('a')
        keyboard.press('c')
        keyboard.release('c')
        keyboard.release(Key.ctrl)
        time.sleep(0.1)
        text = pyperclip.paste()
        if not text:
            logging.info("No text found")
            return
        logging.info(f"Initial text: {text}")
        make_api_call(text)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Define function to fix line
def fix_line():
    logging.info("Starting to inspect line")
    try:
        pyperclip.copy('')    # empty the clipboard for this one
        keyboard.press(Key.ctrl)
        keyboard.press('c')
        keyboard.release('c')
        keyboard.release(Key.ctrl)
        time.sleep(0.1)
        text = pyperclip.paste()
        if not text:
            logging.info("No text found")
            return
        logging.info(f"Initial text: {text}")
        make_api_call(text)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Set up global hotkeys
with pynput.keyboard.GlobalHotKeys({
    PY_CORRECTOR_KEY_COMB_FIX_TEXT: fix_text, 
    PY_CORRECTOR_KEY_COMB_FIX_LINE: fix_line
    }) as h:
    h.join()
