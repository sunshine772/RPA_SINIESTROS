import pyautogui
import time
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
from utils.module_manager import is_logged_in
def ensure_login_and_navigate():
    max_attempts = 3
    for attempt in range(max_attempts):
        img = capture_area("modules")
        texto = extract_text_from_image_with_retries(img)
        if is_logged_in(texto):
            pyautogui.hotkey("alt", "i", "d")
            time.sleep(0.5)
            img_after = capture_area("modules")
            texto_after = extract_text_from_image_with_retries(img_after)
            if "Siniestros*" in texto_after:
                return True
        time.sleep(1)
    return False
