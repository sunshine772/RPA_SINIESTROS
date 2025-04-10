import sys
import time
import pyautogui
import google.generativeai as genai
from actions.program_manager import open_program, focus_program, close_all_programs
from actions.login_manager import detect_login_screen, perform_login
from actions.navigation_manager import ensure_login_and_navigate, navigate_to_policy
from actions.process_manager import process_ci_and_table
from utils.screenshot import capture_modules_area, capture_table_area
from utils.gemini_ocr import extract_text_from_image_with_retries

genai.configure(api_key="AIzaSyAdQbC023CkWj9UfFiUVQRzD6FzG9OwYtQ")

def decide_login_flow(initial_text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Analiza el siguiente texto extraído de una pantalla:
    {initial_text}
    
    Determina si el usuario está logueado en la aplicación 'eL2-QA03-Productos'.
    Busca indicadores como 'login', 'usuario', 'contraseña' (no logueado) o menús como 'Siniestros', 'Administración', etc. (logueado).
    Responde con 'logueado' o 'no_logueado'.
    """
    response = model.generate_content(prompt)
    return response.text.strip() == "logueado"

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ["--ci", "-c"]:
        print("Uso: python main.py --ci 12345678 [--poliza POL-VG-SC-000223-2016-01]")
        return

    ci = None
    poliza = "POL-VG-SC-000223-2016-01"
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] in ["--ci", "-c"]:
            ci = sys.argv[i + 1]
        elif sys.argv[i] == "--poliza":
            poliza = sys.argv[i + 1]

    if not ci:
        print("Error: Debes proporcionar un valor para --ci")
        return

    print("Enfocando el programa 'eL2-QA03-Productos'...")
    focus_program()

    initial_screenshot = capture_modules_area()
    initial_text = extract_text_from_image_with_retries(initial_screenshot)
    print("Texto inicial extraído:\n", initial_text)

    if not decide_login_flow(initial_text):
        print("No estamos logueados. Iniciando proceso de apertura y login...")
        close_all_programs()
        time.sleep(2)  # Delay para asegurar que los procesos se cierren
        open_program()
        time.sleep(5)  # Delay para que la aplicación se abra completamente
        focus_program()  # Reenfocar después de abrir
        if detect_login_screen():
            perform_login()
            time.sleep(2)  # Delay para que el login se complete
            focus_program()  # Reenfocar después del login
    else:
        print("Ya estamos logueados. Procediendo con la navegación...")

    if not ensure_login_and_navigate():
        return

    focus_program()  # Reenfocar antes de procesar la tabla
    table_data = process_ci_and_table(ci)
    print("Tabla procesada:")
    for i, (poliza_key, row) in enumerate(table_data.items(), 1):
        print(f"Fila {i}: {row}")
    
    if not table_data:
        print("La tabla está vacía.")
    else:
        focus_program()  # Reenfocar antes de navegar a la póliza
        navigate_to_policy(table_data, poliza)

if __name__ == "__main__":
    main()
