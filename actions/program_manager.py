import psutil
import pyautogui
import time
import os
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

def open_program():
    pyautogui.hotkey('win')
    pyautogui.write("eL2-QA03-Productos", interval=0.1)
    pyautogui.press("enter")

def focus_program():
    if WIN32_AVAILABLE:
        def enum_windows_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "eL2-QA03-Productos" in title.lower() or "elife2" in title.lower():
                    results.append(hwnd)

        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd = windows[0]
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(hwnd)
            if win32gui.GetWindowPlacement(hwnd)[1] == win32con.SW_MAXIMIZE:
                print("Programa enfocado y maximizado exitosamente usando win32gui.")
            else:
                print("Programa enfocado pero no maximizado. Forzando maximización...")
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        else:
            print("No se encontró la ventana. Intentando reenfocar tras breve espera...")
            time.sleep(2)  # Delay para dar tiempo a que la ventana aparezca
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            if windows:
                hwnd = windows[0]
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
                if win32gui.GetWindowPlacement(hwnd)[1] == win32con.SW_MAXIMIZE:
                    print("Programa enfocado y maximizado tras reintento.")
                else:
                    print("Programa detectado pero no maximizado. Revisa el estado.")
            else:
                print("No se pudo enfocar ni maximizar el programa incluso tras reintento.")
    else:
        print("pywin32 no está disponible. Usando método alternativo...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)  # Delay para el cambio de ventana
        for proc in psutil.process_iter(['pid', 'name']):
            if "eL2" in proc.info['name'].lower() or "elife2" in proc.info['name'].lower():
                print("Programa detectado en procesos. Intentando enfocar...")
                break
        else:
            print("Programa no detectado. Abriendo...")
            open_program()

def close_all_programs():
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if "eL2" in proc.info['name'].lower() or "elife2" in proc.info['name'].lower():
                proc.kill()
                print(f"Cerrado proceso: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
