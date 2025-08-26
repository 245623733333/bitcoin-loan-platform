# loan_agent.py
import os
import asyncio
from typing import Optional

from uagents import Agent, Context, Protocol
from uagents.models import Model

# ----------------------------
# Endpoint (updated by your start_with_ngrok.py)
# This line WILL be overwritten by your script; keep it exactly like this:
endpoint = ""
# ----------------------------

# -------------- ICP client (prefer your icp_client.py) --------------
USE_EXTERNAL_CLIENT = True
try:
    # your helper if it exists
    from icp_client import register_user, take_loan, get_all_users  # type: ignore
    # Optional helpers if you added them later:
    try:
        from icp_client import get_user, repay_loan, deposit_btc, delete_user  # type: ignore
    except Exception:
        get_user = None
        repay_loan = None
        deposit_btc = None
        delete_user = None
except Exception:
    USE_EXTERNAL_CLIENT = False

if not USE_EXTERNAL_CLIENT:
    # fallback: direct ic-py calls
    from ic.client import Client
    from ic.identity import Identity
    from ic.agent import Agent as ICAgent
    from ic.candid import Types, encode, decode

    # --- set these to YOUR backend canister + local replica ---
    CANISTER_ID = os.getenv("ICP_CANISTER_ID", "br5f7-7uaaa-aaaaa-qaaca-cai")
    IC_URL = os.getenv("ICP_URL", "http://127.0.0.1:4943")

    client = Client(url=IC_URL)
    identity = Identity()
    ic_agent = ICAgent(client, identity)
    ic_agent.fetch_root_key()

    async def _update(method: str, args_types, args_vals, ret_type):
        data = encode(args_types, args_vals)
        res = await asyncio.to_thread(ic_agent.update_raw, CANISTER_ID, method, data)
        return decode(ret_type, res)

    async def _query(method: str, args_types, args_vals, ret_type):
        data = encode(args_types, args_vals)
        res = await asyncio.to_thread(ic_agent.query_raw, CANISTER_ID, method, data)
        return decode(ret_type, res)

    async def register_user(name: str):
        return await _update("registerUser", [Types.Text], [name], Types.Text)

    async def take_loan(name: str, amount: int):
        return await _update("takeLoan", [Types.Text, Types.Nat], [name, amount], Types.Text)

    async def repay_loan(name: str, amount: int):
        return await _update("repayLoan", [Types.Text, Types.Nat], [name, amount], Types.Text)

    async def deposit_btc(name: str, amount: int):
        return await _update("depositBTC", [Types.Text, Types.Nat], [name, amount], Types.Text)

    async def get_all_users():
        # vec record { btcBalance:nat; loan:nat; name:text }
        vec_type = Types.Vec(
            Types.Record({"name": Types.Text, "btcBalance": Types.Nat, "loan": Types.Nat})
        )
        return await _query("getAllUsers", [], [], vec_type)

    async def get_user(name: str):
        # opt record { name; btcBalance; loan }
        opt_type = Types.Opt(
            Types.Record({"name": Types.Text, "btcBalance": Types.Nat, "loan": Types.Nat})
        )
        return await _query("getUser", [Types.Text], [name], opt_type)

    async def delete_user(name: str):
        return await _update("deleteUser", [Types.Text], [name], Types.Text)

# -------------- Chat protocol models --------------
class LoanRequest(Model):
    command: str  # e.g., "register Alice", "loan Alice 100", "users"

class LoanResponse(Model):
    reply: str

# Try to also support Fetch.ai's built-in Chat protocol if available
ChatMessage = None
try:
    from uagents.protocols.chat import ChatMessage as _ChatMessage  # type: ignore
    ChatMessage = _ChatMessage
except Exception:
    pass

# -------------- Agent & protocol --------------
loan_protocol = Protocol(name="loan_protocol", version="1.0")

def format_user(u: dict) -> str:
    # handles both list/tuple and dict-like
    if isinstance(u, dict):
        return f"{u.get('name')} | BTC: {u.get('btcBalance')} | Loan: {u.get('loan')}"
    # fallback for tuple-like order (name, btcBalance, loan)
    try:
        return f"{u[0]} | BTC: {u[1]} | Loan: {u[2]}"
    except Exception:
        return str(u)

async def handle_core(ctx: Context, sender: str, text: str) -> str:
    parts = text.strip().split()
    if not parts:
        return "No command. Try: help"

    cmd = parts[0].lower()

    try:
        if cmd in ("help", "?"):
            return (
                "Commands:\n"
                "- register <name>\n"
                "- loan <name> <amount>\n"
                "- repay <name> <amount>\n"
                "- deposit <name> <amount>\n"
                "- user <name>\n"
                "- users\n"
                "- delete <name>\n"
            )

        if cmd == "register" and len(parts) == 2:
            name = parts[1]
            res = await register_user(name)  # type: ignore
            return f"{res}"

        if cmd == "loan" and len(parts) == 3:
            name, amt = parts[1], int(parts[2])
            res = await take_loan(name, amt)  # type: ignore
            return f"{res}"

        if cmd == "repay" and len(parts) == 3 and callable(globals().get("repay_loan")):
            name, amt = parts[1], int(parts[2])
            res = await repay_loan(name, amt)  # type: ignore
            return f"{res}"

        if cmd == "deposit" and len(parts) == 3 and callable(globals().get("deposit_btc")):
            name, amt = parts[1], int(parts[2])
            res = await deposit_btc(name, amt)  # type: ignore
            return f"{res}"

        if cmd == "users":
            users = await get_all_users()  # type: ignore
            if not users:
                return "No users yet."
            lines = [format_user(u) for u in users]
            return "Users:\n" + "\n".join(lines)

        if cmd == "user" and len(parts) == 2 and callable(globals().get("get_user")):
            name = parts[1]
            data = await get_user(name)  # type: ignore
            if not data:
                return f"{name} not found."
            # opt record -> either [] or [record]
            rec = data[0] if isinstance(data, list) and data else data
            return "User:\n" + format_user(rec)

        if cmd == "delete" and len(parts) == 2 and callable(globals().get("delete_user")):
            name = parts[1]
            res = await delete_user(name)  # type: ignore
            return f"{res}"

        return "Unknown or invalid command. Type 'help' for options."
    except Exception as e:
        ctx.logger.exception("Command handling error")
        return f"Error: {e}"

@loan_protocol.on_message(model=LoanRequest, replies=LoanResponse)
async def on_loan_request(ctx: Context, sender: str, msg: LoanRequest):
    reply = await handle_core(ctx, sender, msg.command)
    await ctx.send(sender, LoanResponse(reply=reply))

# Optional: also accept plain ChatMessage if available (Agentverse Chat)
if ChatMessage:
    @loan_protocol.on_message(model=ChatMessage, replies=ChatMessage)  # type: ignore
    async def on_chat(ctx: Context, sender: str, msg: "ChatMessage"):  # type: ignore
        reply = await handle_core(ctx, sender, msg.text)
        await ctx.send(sender, ChatMessage(text=reply))  # type: ignore

# Build the agent
agent_kwargs = dict(name="LoanAgent", seed="loan-agent-seed", port=8000)
# if your ngrok starter injects endpoint="", leave list empty; else include it
if endpoint:
    agent_kwargs["endpoint"] = [endpoint]
loan_agent = Agent(**agent_kwargs)
loan_agent.include(loan_protocol)

if __name__ == "__main__":
    print("LoanAgent running with address:", loan_agent.address)
    # helpful for your scripts to capture address:
    try:
        with open("loan_agent_address.txt", "w") as f:
            f.write(loan_agent.address)
    except Exception:
        pass
    loan_agent.run()
