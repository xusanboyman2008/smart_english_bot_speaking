import psutil
import os
import time

def protect_task():
    # Check if the process is still running
    while True:
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"] == "Copilot.exe":  # Replace with your actual executable name
                time.sleep(100)  # Adjust check interval
                continue
        restart_program()  # Restart if the app is not found

def restart_program():
    # Restart the program if it's not running
    exe_path = "C:/Users/xusanboy/Downloads/Telegram Desktop/Copilot.exe"
    if os.path.exists(exe_path):
        os.system(f'"{exe_path}"')
    else:
        print("Executable not found.")


if __name__ == "__main__":
    protect_task()