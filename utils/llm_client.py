import google.generativeai as genai
import hashlib
_api_key = None
_cache = {}
def configure(api_key: str):
    global _api_key
    _api_key = api_key
    genai.configure(api_key=api_key)
def _cache_key(prompt):
    if isinstance(prompt, list):
        prompt = " ".join(str(p) for p in prompt)
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()
def generate(prompt):
    key = _cache_key(prompt)
    if key in _cache:
        return _cache[key]
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        result = response.text if hasattr(response, "text") else response
        _cache[key] = result
        return result
    except Exception:
        return ""
