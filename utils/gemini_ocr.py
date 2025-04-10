import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyAdQbC023CkWj9UfFiUVQRzD6FzG9OwYtQ")

def extract_text_from_image_with_retries(imagen: Image.Image, max_retries=3) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = """
    Extrae el texto visible de esta imagen de forma clara y precisa.
    Si hay un elemento seleccionado (resaltado o con cursor), añádele un '*' al final.
    Devuelve el texto en líneas separadas si es una tabla.
    """
    for attempt in range(max_retries):
        try:
            response = model.generate_content([prompt, imagen])
            if response and response.text:
                return response.text
            print(f"Intento {attempt + 1} de OCR fallido. Reintentando...")
        except Exception as e:
            print(f"Error en intento {attempt + 1} de OCR: {e}. Reintentando...")
    print("Error: No se pudo extraer texto después de 3 intentos.")
    return ""
