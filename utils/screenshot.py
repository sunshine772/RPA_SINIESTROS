import pyautogui
from PIL import Image
import os
import screeninfo
from utils.gemini_ocr import extract_text_from_image_with_retries
def get_screen_resolution():
    try:
        monitor = screeninfo.get_monitors()[0]
        return monitor.width, monitor.height
    except Exception:
        return 1920, 1080
def calculate_area(area_name):
    screen_width, screen_height = get_screen_resolution()
    areas = {
        "modules": (0.02, 0.0, 0.98, 0.1),
        "table": (0.02, 0.3, 0.22, 0.8),
        "denuncia": (0.1, 0.15, 0.9, 0.8),
        "login": (0.25, 0.25, 0.75, 0.75),
        "center": (0.25, 0.25, 0.75, 0.75),
        "notificaciones": (0.35, 0.40, 0.65, 0.60)
    }
    if area_name not in areas:
        raise ValueError(f"Área desconocida: {area_name}")
    left, top, right, bottom = areas[area_name]
    return (
        int(screen_width * left),
        int(screen_height * top),
        int(screen_width * right),
        int(screen_height * bottom)
    )
def validate_screenshot(area, expected_keywords, retries=2):
    for attempt in range(retries):
        text = extract_text_from_image_with_retries(area)
        if any(keyword.lower() in text.lower() for keyword in expected_keywords):
            return True
        area = pyautogui.screenshot()
    return False
def capture_area(area_name):
    left, top, right, bottom = calculate_area(area_name)
    screenshot = pyautogui.screenshot()
    area = screenshot.crop((left, top, right, bottom))
    expected_keywords = {
        "modules": ["siniestros", "administración", "cotización"],
        "table": ["pol-vg", "pol-apg", "nro.poliza"],
        "denuncia": ["denuncia", "polaza", "asegurado"],
        "login": ["login", "usuario", "contraseña"],
        "center": ["login", "usuario", "contraseña", "siniestros"],
        "notificaciones": ["notificación", "error", "éxito", "aceptar", "cerrar"]
    }
    if validate_screenshot(area, expected_keywords[area_name]):
        os.makedirs("data", exist_ok=True)
        area.save(f"data/{area_name}.png")
        return area
    return screenshot.crop((left, top, right, bottom))
