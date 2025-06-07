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
