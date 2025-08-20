from uagents import Agent, Context, Model
import subprocess

# Model for receiving simple commands
class Command(Model):
    cmd: str

agent = Agent(
    name="loan_agent",
    port=8000,
    seed="loan agent secret"
)

# Function to call Motoko backend using dfx
def call_backend(canister: str, method: str, args: str):
    try:
        result = subprocess.check_output(
            ["dfx", "canister", "call", canister, method, args],
            stderr=subprocess.STDOUT
        )
        return result.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

# Startup: run some initial backend tests
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Agent {agent.name} started!")
    ctx.logger.info(f"Address: {agent.address}")

    ctx.logger.info("Registering Alice...")
    ctx.logger.info(call_backend("bitcoin-loan-backend-backend", "registerUser", '("Alice")'))

    ctx.logger.info("Depositing 50 BTC for Alice...")
    ctx.logger.info(call_backend("bitcoin-loan-backend-backend", "deposit", '("Alice", 50)'))

    ctx.logger.info("Granting loan of 100 BTC to Alice...")
    ctx.logger.info(call_backend("bitcoin-loan-backend-backend", "takeLoan", '("Alice", 100)'))

    ctx.logger.info("Fetching all users...")
    ctx.logger.info(call_backend("bitcoin-loan-backend-backend", "getAllUsers", "()"))

# Handle commands sent to the agent dynamically
@agent.on_message(model=Command)
async def handle_command(ctx: Context, sender: str, msg: Command):
    ctx.logger.info(f"Received command from {sender}: {msg.cmd}")

    parts = msg.cmd.strip().split()
    if not parts:
        await ctx.send(sender, Command(msg="No command provided"))
        return

    action = parts[0].lower()
    response = "Unknown command"

    try:
        if action == "register":
            name = parts[1]
            response = call_backend("bitcoin-loan-backend-backend", "registerUser", f'("{name}")')
        elif action == "deposit":
            name, amount = parts[1], int(parts[2])
            response = call_backend("bitcoin-loan-backend-backend", "deposit", f'("{name}", {amount})')
        elif action == "loan":
            name, amount = parts[1], int(parts[2])
            response = call_backend("bitcoin-loan-backend-backend", "takeLoan", f'("{name}", {amount})')
        elif action == "users":
            response = call_backend("bitcoin-loan-backend-backend", "getAllUsers", "()")
    except Exception as e:
        response = f"Error processing command: {e}"

    await ctx.send(sender, Command(msg=response))

if __name__ == "__main__":
    agent.run()
