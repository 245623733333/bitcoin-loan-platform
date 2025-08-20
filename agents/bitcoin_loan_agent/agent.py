from uagents import Agent, Context, Model
import requests

# --------- Models (what messages look like) ---------
class RegisterUser(Model):
    name: str

class Deposit(Model):
    name: str
    amount: int

class Loan(Model):
    name: str
    amount: int

class Response(Model):
    message: str

# --------- ICP Canister Config ---------
# Replace this with your backend candid URL
CANISTER_API = "http://127.0.0.1:4943"

# --------- Agent Setup ---------
agent = Agent(
    name="bitcoin_loan_agent",
    seed="bitcoin-loan-seed",  # change to secure seed
)

# --------- Handlers ---------

@agent.on_message(model=RegisterUser, replies=Response)
async def register(ctx: Context, sender: str, msg: RegisterUser):
    # ICP backend call (simulate HTTP request, replace with dfx canister call API)
    ctx.logger.info(f"Registering user {msg.name}")
    # TODO: Connect with dfx or canister HTTP outcall
    return Response(message=f"User {msg.name} registered on ICP backend")

@agent.on_message(model=Deposit, replies=Response)
async def deposit(ctx: Context, sender: str, msg: Deposit):
    ctx.logger.info(f"Depositing {msg.amount} for {msg.name}")
    return Response(message=f"Deposited {msg.amount} for {msg.name}")

@agent.on_message(model=Loan, replies=Response)
async def loan(ctx: Context, sender: str, msg: Loan):
    ctx.logger.info(f"Loan request {msg.amount} for {msg.name}")
    return Response(message=f"Loan of {msg.amount} granted to {msg.name}")

# --------- Run Agent ---------
if __name__ == "__main__":
    agent.run()
