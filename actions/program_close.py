import psutil
def close_all_programs():
    for proc in psutil.process_iter(["name"]):
        try:
            if "eL2" in proc.info["name"].lower() or "elife2" in proc.info["name"].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
