import sys
import time
import pyautogui
from actions.program_open import open_program
from actions.program_focus import focus_program
from actions.program_close import close_all_programs
from actions.login_detect import detect_login_screen
from actions.login_perform import perform_login
from actions.navigate_login import ensure_login_and_navigate
from actions.process_ci import process_ci
from actions.parse_table import parse_table, print_policies
from actions.navigate_policy import navigate_policy
from actions.register_denuncia import register_denuncia
from actions.search_again import search_again
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
from utils import llm_client
llm_client.configure(api_key="AIzaSyAdQbC023CkWj9UfFiUVQRzD6FzG9OwYtQ")
def decide_login_flow(initial_text):
    heuristicas = ["siniestros", "administración", "menu", "usuario"]
    if any(word in initial_text.lower() for word in heuristicas):
        return True
    prompt = f"Analiza el siguiente texto:\n{initial_text}\nDetermina si el usuario está logueado en 'eL2-QA03-Productos'.\nResponde con 'logueado' o 'no_logueado'."
    decision = llm_client.generate(prompt).strip()
    return decision == "logueado"
def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ["--ci", "-c"]:
        print("Uso: python main.py --ci 12345678 [--poliza POL-VG-SC-000223-2016-01] [--fecha DD/MM/AAAA]")
        return
    ci = None
    poliza = "POL-VG-SC-000223-2016-01"
    fecha = ""
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] in ["--ci", "-c"]:
            ci = sys.argv[i+1]
        elif sys.argv[i] == "--poliza":
            poliza = sys.argv[i+1]
        elif sys.argv[i] == "--fecha":
            fecha = sys.argv[i+1]
    if not ci:
        print("Error: Debes proporcionar un valor para --ci")
        return
    focus_program()
    initial_screenshot = capture_area("modules")
    initial_text = extract_text_from_image_with_retries(initial_screenshot)
    if not decide_login_flow(initial_text):
        close_all_programs()
        time.sleep(2)
        open_program()
        time.sleep(3)
        focus_program()
        if detect_login_screen():
            perform_login()
            time.sleep(1)
            focus_program()
    if not ensure_login_and_navigate():
        return
    focus_program()
    process_ci(ci)
    table_data = parse_table()
    if not table_data:
        return
    row_index = print_policies(table_data, poliza)
    if row_index >= 0:
        focus_program()
        navigate_policy(table_data, poliza)
        register_denuncia(ci, fecha)
        search_again(ci)
if __name__ == "__main__":
    main()
