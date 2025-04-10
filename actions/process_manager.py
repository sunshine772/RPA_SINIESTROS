import pyautogui
import time
import pyperclip
from utils.screenshot import capture_table_area
from utils.gemini_ocr import extract_text_from_image_with_retries

def process_ci_and_table(ci):
    pyautogui.hotkey("alt", "i")
    pyautogui.press("d")
    for _ in range(5):
        pyautogui.press("tab")
    pyperclip.copy(ci)
    pyautogui.hotkey("ctrl", "v")
    for _ in range(3):
        pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(5)  # Delay para que la tabla cargue
    tabla = capture_table_area()
    raw_text = extract_text_from_image_with_retries(tabla)
    print("Texto crudo de la tabla:\n", raw_text)
    return parse_table(raw_text)

def parse_table(texto_tabla):
    lines = texto_tabla.strip().split('\n')
    headers = ["Nro.Poliza", "Nombre Asegurado", "Doc.Identidad", "Fecha Nac.", "Grupo/Cartera", 
               "Movimiento", "Inicio Vigencia", "Termino Vigencia", "Nombre Contratante", "Producto"]
    table_data = {}
    current_poliza = None
    current_data = []
    
    for line in lines:
        line = line.strip()
        if any(p in line for p in ["POL-VG", "POL-APG"]):
            if current_poliza and current_data:
                table_data[current_poliza] = process_policy_data(current_poliza, current_data, headers)
            current_poliza = line.split()[0].replace("*", "")
            current_data = [line]
        elif current_poliza and line:
            current_data.append(line)
    
    if current_poliza and current_data:
        table_data[current_poliza] = process_policy_data(current_poliza, current_data, headers)
    
    return table_data

def process_policy_data(poliza, data_lines, headers):
    full_text = " ".join(data_lines)
    parts = full_text.split()
    ci_index = parts.index("6376282") if "6376282" in parts else -1
    if ci_index == -1:
        return {}
    
    fecha_index = ci_index + 1
    grupo_start = fecha_index + 1
    grupo_end = grupo_start + (2 if "SANTA CRUZ" in full_text else 1)
    movimiento_index = grupo_end
    inicio_index = movimiento_index + 1
    termino_index = inicio_index + 1
    contratante_start = termino_index + 1
    producto_start = contratante_start + 4  # "CONECTA REDES Y SERVICIOS" tiene 4 palabras
    
    return {
        "Nro.Poliza": poliza,
        "Nombre Asegurado": " ".join(parts[1:ci_index]),
        "Doc.Identidad": parts[ci_index],
        "Fecha Nac.": parts[fecha_index],
        "Grupo/Cartera": " ".join(parts[grupo_start:grupo_end]),
        "Movimiento": parts[movimiento_index],
        "Inicio Vigencia": parts[inicio_index],
        "Termino Vigencia": parts[termino_index],
        "Nombre Contratante": " ".join(parts[contratante_start:producto_start]),
        "Producto": " ".join(parts[producto_start:])
    }
