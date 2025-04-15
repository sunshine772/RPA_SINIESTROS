import pyautogui
import time
import pyperclip
def process_ci(ci):
    for _ in range(5):
        pyautogui.press("tab", interval=0.1)
    pyperclip.copy(ci)
    pyautogui.hotkey("ctrl", "v")
    for _ in range(3):
        pyautogui.press("tab", interval=0.1)
    pyautogui.press("enter")
    time.sleep(5)
