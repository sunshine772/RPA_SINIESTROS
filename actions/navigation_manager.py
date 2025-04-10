import pyautogui
import time
from utils.screenshot import capture_modules_area, capture_table_area
from utils.gemini_ocr import extract_text_from_image_with_retries
from utils.module_manager import is_logged_in

def ensure_login_and_navigate():
    max_attempts = 3
    for attempt in range(max_attempts):
        img = capture_modules_area()
        texto = extract_text_from_image_with_retries(img)
        print(f"Intento {attempt + 1} - Texto extraído:\n", texto)
        
        if is_logged_in(texto):
            print("Login confirmado.")
            print("Navegando a 'Siniestros' con atajo Alt + I.")
            pyautogui.hotkey('alt', 'i')
            time.sleep(1)  # Delay para que la navegación se complete
            img_after = capture_modules_area()
            texto_after = extract_text_from_image_with_retries(img_after)
            print("Texto después de navegar:\n", texto_after)
            if "Siniestros*" in texto_after:
                print("Navegación a 'Siniestros' confirmada.")
                return True
            else:
                print("Fallo en la navegación. Reintentando...")
        else:
            print("Login fallido. Reintentando...")
    print("Error: No se pudo confirmar login o navegación.")
    return False

def navigate_to_policy(table_data, target_policy):
    if target_policy in table_data:
        row_index = list(table_data.keys()).index(target_policy)
        print(f"Póliza '{target_policy}' encontrada en la fila {row_index + 1}. Navegando con tab y flechas...")
        
        # Entrar a la tabla desde el estado post-búsqueda
        pyautogui.press('tab')  # Posicionar el foco antes de la tabla
        time.sleep(0.5)  # Delay para estabilizar
        pyautogui.press('down')  # Primera flecha para llegar a la fila 1
        time.sleep(0.2)  # Delay para estabilizar
        
        # Navegar a la fila objetivo (row_index flechas adicionales)
        for _ in range(row_index):
            pyautogui.press('down')
            time.sleep(0.2)  # Delay entre flechas
        
        # Verificación simple (sin OCR redundante)
        print(f"Navegación a la póliza '{target_policy}' completada con 1 + {row_index} flechas abajo.")
    else:
        print(f"No se encontró la póliza '{target_policy}' en la tabla.")
