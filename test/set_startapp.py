import os
import winreg as reg
import subprocess
import time
import sys

def run_as_admin():
    """ Re-launch the script as administrator if not already running with admin privileges """
    if not is_admin():
        script = sys.argv[0]
        params = " ".join(sys.argv[1:])
        # Ensure the executable path and script path are quoted properly
        command = f'runas /user:Administrator "cmd.exe /c python \"{sys.executable}\" \"{script}\" {params}"'
        print(f"Running with command: {command}")
        subprocess.run(command, shell=True)
        sys.exit()

def is_admin():
    """ Check if the script is running with administrator privileges """
    try:
        return os.geteuid() == 0  # This works on Unix-based systems, but for Windows, use `os` or `ctypes`
    except AttributeError:
        return False

def add_to_startup(app_name="MyApp"):
    try:
        exe_path = os.path.abspath(__file__)  # Full path to the current script

        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_SET_VALUE)

        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, exe_path)
        reg.CloseKey(reg_key)
    except Exception:
        pass

def remove_from_startup():
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)

        try:
            reg.QueryValueEx(reg_key, "MyApp")
            reg.DeleteValue(reg_key, "MyApp")
            print("Successfully removed MyApp from startup.")
        except FileNotFoundError:
            print("Registry entry 'MyApp' not found. It may have already been removed.")

        reg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error removing from startup: {e}")

def run_exe_for_duration(exe_name, duration=10):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(script_dir, exe_name)

        process = subprocess.Popen(exe_path)
        print(f"Started {exe_name}, will stop after {duration} seconds...")

        time.sleep(duration)

        process.terminate()
        print(f"Stopped {exe_name} after {duration} seconds.")
    except Exception as e:
        print(f"Error: {e}")

