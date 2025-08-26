import os
import json
import requests
import subprocess
import time

# Path to your loan_agent.py
LOAN_AGENT_PATH = "loan_agent.py"
NGROK_API_URL = "http://127.0.0.1:4040/api/tunnels"

def kill_old_ngrok():
    print("Killing old ngrok processes...")
    try:
        result = subprocess.run(["pgrep", "-u", os.getlogin(), "ngrok"], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")

        for pid in pids:
            if pid:
                os.kill(int(pid), 9)
        print("Old ngrok processes killed.")
    except Exception as e:
        print("No old ngrok processes found or error:", e)

def get_existing_ngrok_url():
    try:
        res = requests.get(NGROK_API_URL).json()
        tunnels = res.get("tunnels", [])
        for t in tunnels:
            if t["proto"] == "https":
                return t["public_url"]
    except:
        return None
    return None

def start_ngrok():
    print("Starting ngrok tunnel...")
    subprocess.Popen(["ngrok", "http", "8000"])
    time.sleep(3)  # wait for ngrok to start
    return get_existing_ngrok_url()

def update_loan_agent_endpoint(file_path, new_url):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return
    with open(file_path, "r") as f:
        content = f.read()

    # Replace existing endpoint= line or add if missing
    if "endpoint=" in content:
        lines = content.split("\n")
        for i in range(len(lines)):
            if lines[i].startswith("endpoint="):
                lines[i] = f'endpoint="{new_url}"'
        new_content = "\n".join(lines)
    else:
        new_content = content + f'\nendpoint="{new_url}"\n'

    with open(file_path, "w") as f:
        f.write(new_content)
    print(f"Updated {file_path} with new endpoint: {new_url}")

if __name__ == "__main__":
    kill_old_ngrok()
    url = get_existing_ngrok_url()

    if not url:
        url = start_ngrok()

    if url:
        print(f"Ngrok URL: {url}")
        update_loan_agent_endpoint(LOAN_AGENT_PATH, url)
    else:
        print("Failed to get ngrok URL. Check ngrok logs.")
