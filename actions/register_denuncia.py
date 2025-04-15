import pyautogui
import time
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
from utils import llm_client
def get_start_date():
    img = capture_area("denuncia")
    text = extract_text_from_image_with_retries(img)
    prompt = f"Extrae la fecha de inicio de este formulario:\n{text}\nDevuelve la fecha en formato DD/MM/AAAA."
    fecha = llm_client.generate(prompt).strip()
    return fecha
def decide_notification_action(notif_text):
    prompt = f"Analiza el siguiente texto de una notificación:\n{notif_text}\nDetermina cuántas notificaciones hay y cómo cerrarlas. Las opciones para cerrar son:\n- 'tab_enter': Presionar Tab y luego Enter.\n- 'tab_tab_enter': Presionar Tab, Tab y luego Enter.\nDevuelve un JSON con:\n- 'count': número de notificaciones (1 o 2).\n- 'action': 'tab_enter' o 'tab_tab_enter'."
    response = llm_client.generate(prompt).strip()
    try:
        return json.loads(response)
    except:
        return {"count": 1, "action": "tab_enter"}
def handle_notifications():
    screenshot = capture_area("notificaciones")
    notif_text = extract_text_from_image_with_retries(screenshot)
    decision = decide_notification_action(notif_text)
    count = decision.get("count", 1)
    action = decision.get("action", "tab_enter")
    for i in range(min(count, 2)):
        if action == "tab_enter":
            pyautogui.press("tab", interval=0.1)
            pyautogui.press("enter")
        elif action == "tab_tab_enter":
            for _ in range(2):
                pyautogui.press("tab", interval=0.1)
            pyautogui.press("enter")
        else:
            pyautogui.press("tab", interval=0.1)
            pyautogui.press("enter")
        if i < count - 1:
            time.sleep(1)
            screenshot = capture_area("notificaciones")
            notif_text = extract_text_from_image_with_retries(screenshot)
def register_denuncia(ci, fecha=""):
    if not fecha:
        fecha = get_start_date()
    for _ in range(5):
        pyautogui.press("left", interval=0.1)
    for _ in range(11):
        pyautogui.press("tab", interval=0.1)
    pyautogui.press("left", interval=0.1)
    for _ in range(13):
        pyautogui.press("tab", interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)
    handle_notifications()
    time.sleep(1)
    pyautogui.hotkey("alt", "i")
    pyautogui.press("a")
    for _ in range(2):
        pyautogui.press("tab", interval=0.1)
    for _ in range(3):
        pyautogui.press("right", interval=0.1)
    for _ in range(4):
        pyautogui.press("tab", interval=0.1)
    pyautogui.write(ci, interval=0.1)
    for _ in range(2):
        pyautogui.press("tab", interval=0.1)
    pyautogui.press("enter")
