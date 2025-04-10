import pyautogui
from PIL import Image
import os

def capture_modules_area():
    os.makedirs("data", exist_ok=True)
    screenshot = pyautogui.screenshot()
    ancho, _ = screenshot.size
    area = screenshot.crop((0, 0, ancho, 100))
    area.save("data/modulos.png")
    return area

def capture_table_area():
    os.makedirs("data", exist_ok=True)
    screenshot = pyautogui.screenshot()
    ancho, alto = screenshot.size
    altura_original = alto - 350
    recorte_top = altura_original * 0.3
    nuevo_top = 150 + recorte_top
    recorte_lateral = ancho * 0.02
    nuevo_left = recorte_lateral
    nuevo_right = ancho - recorte_lateral
    area = screenshot.crop((nuevo_left, nuevo_top, nuevo_right, alto - 200))
    area.save("data/tabla.png")
    return area
    
def capture_screen_center():
    os.makedirs("data", exist_ok=True)
    screenshot = pyautogui.screenshot()
    ancho, alto = screenshot.size
    area = screenshot.crop((ancho//4, alto//4, 3*ancho//4, 3*alto//4))
    area.save("data/centro.png")
    return area
