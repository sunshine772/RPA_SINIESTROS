import pyautogui
import time
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
def navigate_policy(table_data, target_policy):
    if target_policy not in table_data:
        return
    row_index = list(table_data.keys()).index(target_policy)
    pyautogui.press("tab")
    pyautogui.press("home")
    for _ in range(row_index):
        pyautogui.press("down", interval=0.1)
    for _ in range(2):
        pyautogui.press("alt", interval=0.1)
    for _ in range(3):
        pyautogui.hotkey("shift", "tab", interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)
    denuncia_img = capture_area("denuncia")
    resultado = extract_text_from_image_with_retries(denuncia_img)
    if target_policy not in resultado:
        return
