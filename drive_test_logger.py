import os
import sys
import hashlib
import urllib.request

GITHUB_RAW_URL = "https://raw.githubusercontent.com/BCEVM/drive_test_logger/main/drive_test_logger.py"
LOCAL_FILE = os.path.abspath(__file__)

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def get_remote_hash(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return hashlib.sha256(data).hexdigest(), data

def check_for_update():
    try:
        local_hash = get_file_hash(LOCAL_FILE)
        remote_hash, remote_data = get_remote_hash(GITHUB_RAW_URL)

        if local_hash != remote_hash:
            print("[*] Update available! Downloading latest version...")
            with open(LOCAL_FILE, "wb") as f:
                f.write(remote_data)
            print("[+] Script updated. Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("[=] Script is up-to-date.")
    except Exception as e:
        print(f"[!] Update check failed: {e}")

check_for_update()
