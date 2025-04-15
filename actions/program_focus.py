import psutil
import pyautogui
import time
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
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
        else:
            time.sleep(2)
            win32gui.EnumWindows(enum_windows_callback, windows)
            if windows:
                hwnd = windows[0]
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
    else:
        pyautogui.hotkey("alt", "tab")
        time.sleep(1)
        for proc in psutil.process_iter(["name"]):
            if "eL2" in proc.info["name"].lower() or "elife2" in proc.info["name"].lower():
                break
