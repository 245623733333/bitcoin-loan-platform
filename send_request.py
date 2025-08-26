from uagents import Agent, Context, Model
from loan_agent import Ping, Pong

with open("loan_agent_address.txt", "r") as f:
    LOAN_ADDR = f.read().strip()

test_client = Agent(
    name="TestClient",
    seed="test_client_seed",
    port=8001,
    endpoint="https://6ba6929663f8.ngrok-free.app"
)

@test_client.on_event("startup")
async def startup(ctx: Context):
    await ctx.send(LOAN_ADDR, Ping(text="Ping?"))
    ctx.logger.info("Ping sent.")

@test_client.on_message(model=Pong)
async def handle_pong(ctx: Context, sender: str, msg: Pong):
    ctx.logger.info(f"Got from LoanAgent: {msg.reply}")

if __name__ == "__main__":
    test_client.run()
