import os
import sys
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/BCEVM/drive_test_logger.git"
LOCAL_DIR = Path("drive_test_logger")
MAIN_SCRIPT = LOCAL_DIR / "drive_test_logger.py"

def clone_or_update_repo():
    if not LOCAL_DIR.exists():
        print("[*] Cloning repo...")
        subprocess.run(["git", "clone", REPO_URL, str(LOCAL_DIR)], check=True)
    else:
        print("[*] Pulling latest changes...")
        subprocess.run(["git", "-C", str(LOCAL_DIR), "pull"], check=True)

def run_main_script():
    print(f"[+] Running {MAIN_SCRIPT}...")
    subprocess.run([sys.executable, str(MAIN_SCRIPT)])

if __name__ == "__main__":
    try:
        clone_or_update_repo()
        run_main_script()
    except Exception as e:
        print(f"[!] Error: {e}")
