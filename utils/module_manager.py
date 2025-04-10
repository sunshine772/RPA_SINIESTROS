import unicodedata

EXPECTED_MODULES = [
    "Administración", "Cotización", "Suscripción", "Emisión", "Mantenimiento",
    "Cobranza", "Siniestros", "Reaseguros", "Consultas", "Reservas", "Contabilidad"
]

def normalize_text(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')

def is_logged_in(texto: str) -> bool:
    texto_clean = texto.replace("*", "").lower()
    return all(normalize_text(mod) in normalize_text(texto_clean) for mod in EXPECTED_MODULES) and "siniestros" in texto_clean
