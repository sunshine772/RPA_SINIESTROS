import pyautogui
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
def detect_login_screen():
    screenshot = capture_area("login")
    texto = extract_text_from_image_with_retries(screenshot)
    return any(word in texto.lower() for word in ["login", "usuario", "contraseña"])
