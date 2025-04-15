import pyautogui
def open_program():
    pyautogui.hotkey("win")
    pyautogui.write("eL2-QA03-Productos", interval=0.1)
    pyautogui.press("enter")
