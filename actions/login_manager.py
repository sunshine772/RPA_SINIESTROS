import pyautogui
from utils.screenshot import capture_screen_center
from utils.gemini_ocr import extract_text_from_image_with_retries

def detect_login_screen():
    screenshot = capture_screen_center()
    texto = extract_text_from_image_with_retries(screenshot)
    return "login" in texto.lower() or "usuario" in texto.lower() or "contraseña" in texto.lower()

def perform_login():
    pyautogui.write("starifa", interval=0.2)
    pyautogui.press('tab')
    pyautogui.write("Nacional25*", interval=0.2)
    pyautogui.press('enter')
