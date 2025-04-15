import json
from utils.screenshot import capture_area
from utils.gemini_ocr import extract_text_from_image_with_retries
from utils import llm_client
def decide_policy_presence(raw_text):
    heuristicas = ["POL-VG", "POL-APG"]
    if any(word in raw_text for word in heuristicas):
        return True
    prompt = f"Analiza el siguiente texto:\n{raw_text}\nDetermina si hay pólizas presentes (e.g., comienzan con 'POL-VG' o 'POL-APG').\nResponde con 'presentes' o 'no_presentes'."
    decision = llm_client.generate(prompt).strip()
    return decision == "presentes"
def parse_table():
    tabla = capture_area("table")
    raw_text = extract_text_from_image_with_retries(tabla)
    if not decide_policy_presence(raw_text):
        return {}
    cleaned_text = "\n".join(line.strip() for line in raw_text.split("\n") if line.strip())
    prompt = f"Dada la siguiente salida de OCR de una tabla:\n{cleaned_text}\nExtrae las pólizas y sus datos en un formato estructurado. Devuelve una lista de diccionarios con las siguientes claves:\n- Nro.Poliza\n- Nombre Asegurado\n- Doc.Identidad\n- Fecha Nac.\n- Grupo/Cartera\n- Movimiento\n- Inicio Vigencia\n- Termino Vigencia\n- Nombre Contratante\n- Producto\nCada diccionario debe corresponder a una fila de la tabla. Las pólizas comienzan con 'POL-VG' o 'POL-APG'.\nIgnora líneas vacías o irrelevantes. Si no puedes parsear un campo, déjalo como cadena vacía ('').\nDevuelve el resultado en formato JSON."
    try:
        response = llm_client.generate(prompt)
        table_data = json.loads(response.strip())
        return {row["Nro.Poliza"]: row for row in table_data}
    except Exception:
        return parse_table_fallback(cleaned_text)
def parse_table_fallback(texto_tabla):
    lines = texto_tabla.strip().split("\n")
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
    try:
        ci_index = parts.index("6376282")
    except ValueError:
        return {h: "" for h in headers}
    fecha_index = ci_index + 1
    grupo_start = fecha_index + 1
    grupo_end = grupo_start + (2 if "SANTA CRUZ" in full_text else 1)
    movimiento_index = grupo_end
    inicio_index = movimiento_index + 1
    termino_index = inicio_index + 1
    contratante_start = termino_index + 1
    producto_start = contratante_start + 4
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
def print_policies(table_data, target_policy):
    for i, poliza in enumerate(table_data.keys()):
        marker = " *" if poliza == target_policy else ""
        print(f"Fila {i}: {poliza}{marker}")
    return list(table_data.keys()).index(target_policy) if target_policy in table_data else -1
