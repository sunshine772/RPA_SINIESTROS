import google.generativeai as genai
from PIL import Image
def extract_text_from_image_with_retries(imagen: Image.Image, max_retries=3) -> str:
    prompt = "Extrae el texto visible de esta imagen de forma clara y precisa.\nSi hay un elemento seleccionado (resaltado o con cursor), añádele un '*' al final.\nDevuelve el texto en líneas separadas si es una tabla."
    from utils import llm_client
    for attempt in range(max_retries):
        try:
            response = llm_client.generate([prompt, imagen])
            if response:
                return response
        except Exception:
            pass
    return ""
