# run_all.py
import os, subprocess, time, requests, sys

NGROK_API = "http://127.0.0.1:4040/api/tunnels"

def start(cmd, name):
    print(f"starting {name} ...")
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def ensure_dfx():
    # start replica if not already
    subprocess.run(["dfx", "start", "--background"], check=False)
    subprocess.run(["dfx", "deploy"], check=True)

def ngrok_url():
    try:
        r = requests.get(NGROK_API, timeout=2).json()
        for t in r.get("tunnels", []):
            if t.get("proto") == "https":
                return t["public_url"]
    except Exception:
        return None

if __name__ == "__main__":
    ensure_dfx()

    # start fastapi
    api = start([sys.executable, "main.py"], "api")
    time.sleep(1)

    # start agent
    agent = start([sys.executable, "loan_agent.py"], "agent")
    time.sleep(1)

    # start ngrok for agent port 8000
    subprocess.run(["pkill", "ngrok"], check=False)
    ng = start(["ngrok", "http", "8000"], "ngrok")
    time.sleep(3)

    url = ngrok_url()
    print("\n=== SERVICES ===")
    print("FastAPI: http://127.0.0.1:8000")
    if url:
        print(f"Agent (ngrok): {url}")
        # grab address from file if you store it; otherwise ask to copy from console
        print("Open Agentverse Inspector with:")
        print(f"https://agentverse.ai/inspect/?uri={url}&address=<PASTE_LOAN_AGENT_ADDRESS_FROM_CONSOLE>")
    else:
        print("ngrok url not found; is ngrok running?")
    print("================\n")

    # keep processes alive
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        for p in (api, agent, ng):
            if p: p.terminate()
