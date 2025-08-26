from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# ====== YOUR MAILBOX TOKEN ======
MAILBOX_TOKEN = "eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3NjM3MTYxODAsImlhdCI6MTc1NTk0MDE4MCwiaXNzIjoiZmV0Y2guYWkiLCJqdGkiOiIwMDZjZmQwZGJkNzUyYjhlZTQ4NGMzMWEiLCJzY29wZSI6ImF2Iiwic3ViIjoiMmFiY2NlNThiYTcwMDYzY2EwOGQwMWM2ZWJlYTc1YzY1M2Q5ZWYzN2Q4OGQyOWM2In0.hrnRuj4ZrPwmIw3bmMB4a4j2qH5r13ANR8tzQ3hkSbGMBdq7JSpL3myuhUxgJVV9ka46giNc39q3s4m_v8u-UkZbtDlKTt3iqlGU98jQPUgAp-rL52tKk8zAD_X9kwKQgNNVZnSt6gm8x5sdJ56rfQyByg9F6eoF34c0ann5To58HhbLFaKv5xNcgByLwKVdxE16JSpKFjLyFIQzVaJhQTyg4FK4siPGtY3rca3lu0AYgKyMPhtxplKGqEms64hbwdtmhdrIP4RCeNkXaSrNBUWKq0HDiQ6MI60EqUBS9O5NEeRwigR91Ufxy1Uq4rNn8R2lUfhHzvMl94HKI3TRwA"

# ====== CREATE AGENT WITH MAILBOX ======
agent = Agent(
    name="Bitcoin Loan Agent",
    seed="bitcoin-loan-seed",
    mailbox=f"https://agentverse.ai/mailbox/{MAILBOX_TOKEN}",
)

# Fund the agent on testnet if low
fund_agent_if_low(agent.wallet.address())

# ====== DEFINE MESSAGE TYPES ======
class LoanRequest(Model):
    amount: float
    duration: int  # in days


class LoanResponse(Model):
    message: str


# ====== MESSAGE HANDLER ======
@agent.on_message(model=LoanRequest, replies=LoanResponse)
async def handle_loan_request(ctx: Context, sender: str, msg: LoanRequest):
    ctx.logger.info(f"Loan request: {msg.amount} BTC for {msg.duration} days")

    # Simple approval logic
    if msg.amount <= 1.0:
        response = f"Loan of {msg.amount} BTC approved for {msg.duration} days!"
    else:
        response = f"Loan request for {msg.amount} BTC denied. Max allowed is 1 BTC."

    await ctx.send(sender, LoanResponse(message=response))


# ====== START AGENT ======
if __name__ == "__main__":
    agent.run()
