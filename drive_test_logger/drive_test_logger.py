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

import os
import json
import time
import pandas as pd
from datetime import datetime

output_file = "drive_test_log.csv"

def get_location():
    loc = os.popen("termux-location -p gps").read()
    return json.loads(loc) if loc else {}

def get_cell_info():
    cell = os.popen("termux-telephony-cellinfo").read()
    return json.loads(cell) if cell else {}

def log_data():
    location = get_location()
    cellinfo = get_cell_info()
    timestamp = datetime.now().isoformat()

    logs = []

    if cellinfo and "cellInfo" in cellinfo:
        for info in cellinfo["cellInfo"]:
            data = {
                "timestamp": timestamp,
                "lat": location.get("latitude"),
                "lon": location.get("longitude"),
                "provider": location.get("provider"),
                "type": info.get("type"),
                "mcc": info.get("cellIdentity", {}).get("mcc"),
                "mnc": info.get("cellIdentity", {}).get("mnc"),
                "cellId": info.get("cellIdentity", {}).get("ci") or info.get("cellIdentity", {}).get("cid"),
                "rsrp": info.get("cellSignalStrength", {}).get("rsrp"),
                "rsrq": info.get("cellSignalStrength", {}).get("rsrq"),
                "signal_strength": info.get("cellSignalStrength", {}).get("dbm"),
            }
            logs.append(data)

    return logs

def save_to_csv(data):
    df = pd.DataFrame(data)
    if not os.path.isfile(output_file):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, mode='a', header=False, index=False)

# Main loop
try:
    while True:
        entries = log_data()
        if entries:
            save_to_csv(entries)
            print(f"[+] Logged {len(entries)} entries at {datetime.now()}")
        else:
            print("[-] No data captured...")
        time.sleep(10)  # delay antar log (detik)
except KeyboardInterrupt:
    print("\n[!] Logging stopped.")
