#!/usr/bin/env python3

import requests
import subprocess
import psutil
import time
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
service_url = "https://cloud.myrapidtrack.com:8443"
timeout = 15
target_cmd = "python /home/voice-recognition/app.py"

def log(msg):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

def check_service(url, timeout):
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def stop_service():
    subprocess.run(["supervisorctl", "stop", "voice"], check=False)

def start_service():
    subprocess.run(["supervisorctl", "start", "voice"], check=False)

def kill_matching_processes(target_string):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'])
            if target_string in cmdline:
                log(f"Killing process PID {proc.info['pid']}: {cmdline}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    if check_service(service_url, timeout):
        log("Voice Service is healthy. Nothing to do.")
        return
    log("Voice Service not healthy. Restarting...")
    # Stop Supervisor service
    stop_service()

    # Kill any remaining python processes matching
    kill_matching_processes(target_cmd)

    # Give it a moment before restarting
    time.sleep(5)

    # Start Supervisor service
    start_service()

if __name__ == "__main__":
    main()
