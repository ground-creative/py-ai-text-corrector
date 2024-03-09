import os, subprocess, time, pynput, pyautogui, pyperclip
from pynput.keyboard import Key, Controller
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PY_CORRECTOR_KEY_COMB_FIX_TEXT = os.getenv('PY_CORRECTOR_KEY_COMB_FIX_TEXT')
PY_CORRECTOR_KEY_COMB_FIX_LINE = os.getenv('PY_CORRECTOR_KEY_COMB_FIX_LINE')
PY_CORRECTOR_AI_ADDRESS = os.getenv('PY_CORRECTOR_AI_ADDRESS')
PY_CORRECTOR_API_KEY = os.getenv('PY_CORRECTOR_API_KEY')
PY_CORRECTOR_AI_RULE = os.getenv('PY_CORRECTOR_AI_RULE')

client = OpenAI(base_url=PY_CORRECTOR_AI_ADDRESS, api_key=PY_CORRECTOR_API_KEY)
keyboard = Controller()

def make_api_call(text):
	completion = client.chat.completions.create(
	model="local-model", # this field is currently unused
	messages=[
		{
			"role": "user", 
			"content": f"""{PY_CORRECTOR_AI_RULE}:{text}"""}
		],
		temperature=0.7,
	)
	final = completion.choices[0].message.content
	if final is not None:
		print("Final text: {}".format(final))
		pyperclip.copy(final)
		time.sleep(0.1)
		pyautogui.hotkey('ctrl', 'v')
			
def fix_text():
	print("Starting to inspect text");
	try:
		pyperclip.copy('')	# empty the clipboard for this one
		keyboard.press(Key.ctrl)
		keyboard.press('a')
		keyboard.release('a')
		keyboard.press('c')
		keyboard.release('c')
		keyboard.release(Key.ctrl)
		time.sleep(0.1)
		text = pyperclip.paste()
		if not text:
			print("No text found")
			return
		print("Inital text: {}".format(text))
		make_api_call(text)
	except Exception as e:
		print("An error occurred: ", e)
		
def fix_line():
	print("Starting to inspect line");
	try:	
		pyperclip.copy('')	# empty the clipboard for this one
		keyboard.press(Key.ctrl)
		#keyboard.press('a')
		#keyboard.release('a')
		keyboard.press('c')
		keyboard.release('c')
		keyboard.release(Key.ctrl)
		time.sleep(0.1)
		text = pyperclip.paste()
		if not text:
			print("No text found")
			return
		print("Inital text: {}".format(text))
		make_api_call(text)
	except Exception as e:
		print("An error occurred: ", e)

with pynput.keyboard.GlobalHotKeys(
	{
		PY_CORRECTOR_KEY_COMB_FIX_TEXT: fix_text, 
		PY_CORRECTOR_KEY_COMB_FIX_LINE: fix_line
	}) as h:
	h.join()