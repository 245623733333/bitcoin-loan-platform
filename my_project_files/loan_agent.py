from uagents import Agent, Context, Model

class Ping(Model):
    text: str

class Pong(Model):
    reply: str

loan_agent = Agent(
    name="LoanAgent",
    seed="loan_agent_seed",
    port=8000,
    endpoint="http://127.0.0.1:8000/submit"
)

print("LoanAgent endpoint:",  "https://6ba6929663f8.ngrok-free.app")
@loan_agent.on_message(model=Ping)
async def handle_ping(ctx: Context, sender: str, msg: Ping):
    ctx.logger.info(f"Received: {msg.text}")
    await ctx.send(sender, Pong(reply="Pong!"))

if __name__ == "__main__":
    loan_agent.run()
