import pyautogui
import time
import pyperclip
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
def search_again(ci):
    pyautogui.hotkey("alt", "i")
    pyautogui.press("a")
    time.sleep(2)
    img = capture_area("modules")
    texto = extract_text_from_image_with_retries(img)
    for _ in range(5):
        pyautogui.press("tab", interval=0.1)
    pyperclip.copy(ci)
    pyautogui.hotkey("ctrl", "v")
    for _ in range(3):
        pyautogui.press("tab", interval=0.1)
    pyautogui.press("enter")
    time.sleep(5)
