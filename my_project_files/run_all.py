import subprocess
import time
import requests
from uagents import Agent, Model  # No 'run' import

# --- Define Message Models ---
class Ping(Model):
    message: str

class Pong(Model):
    message: str

# --- Start ngrok tunnel ---
print("Starting ngrok tunnel...")
ngrok = subprocess.Popen(["ngrok", "http", "8000"])
time.sleep(3)
try:
    tunnel_url = requests.get("http://localhost:4040/api/tunnels").json()['tunnels'][0]['public_url']
except:
    tunnel_url = "http://127.0.0.1:8000"
print("Ngrok URL:", tunnel_url)

# --- Create Agents ---
loan_agent = Agent(name="LoanAgent", port=8000, seed="loan_seed")
test_client = Agent(name="TestClient", port=8001, seed="client_seed")

# --- Define Endpoints ---
loan_endpoint = f"{tunnel_url}/submit"
print("LoanAgent endpoint:", loan_endpoint)

# --- Message Handlers ---
@loan_agent.on_message(Ping, replies=Pong)
async def handle_ping(ctx, sender, msg):
    print(f"Ping received from {sender}: {msg.message}")
    await ctx.send(sender, Pong(message="Pong from LoanAgent"))

@test_client.on_interval(5.0)
async def send_ping(ctx):
    await ctx.send(loan_agent.address, Ping(message="Hello LoanAgent"))
    print("Ping sent.")

# --- Run Agents ---
loan_agent.run()
test_client.run()
