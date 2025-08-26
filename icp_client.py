# icp_client.py
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import Types, encode, decode
from typing import List, Dict, Optional

IC_URL = "http://127.0.0.1:4943"
CANISTER_ID = "br5f7-7uaaa-aaaaa-qaaca-cai"  # <-- set to the canister that has the methods you listed

_client = Client(IC_URL)
_identity = Identity()  # anonymous for local
_agent = Agent(_client, _identity)
_agent.fetch_root_key()

def _update(method: str, arg_types, args, ret_types):
    data = encode(arg_types, args)
    raw = _agent.update_raw(CANISTER_ID, method, data)
    return decode(ret_types, raw)

def _query(method: str, arg_types, args, ret_types):
    data = encode(arg_types, args)
    raw = _agent.query_raw(CANISTER_ID, method, data)
    return decode(ret_types, raw)

def register_user(name: str) -> str:
    return _update("registerUser", [Types.Text], [name], [Types.Text])[0]

def take_loan(name: str, amount: int) -> str:
    return _update("takeLoan", [Types.Text, Types.Nat], [name, amount], [Types.Text])[0]

def repay_loan(name: str, amount: int) -> str:
    return _update("repayLoan", [Types.Text, Types.Nat], [name, amount], [Types.Text])[0]

def deposit_btc(name: str, amount: int) -> str:
    return _update("depositBTC", [Types.Text, Types.Nat], [name, amount], [Types.Text])[0]

def delete_user(name: str) -> str:
    return _update("deleteUser", [Types.Text], [name], [Types.Text])[0]

def get_user(name: str) -> Optional[Dict]:
    res = _query("getUser", [Types.Text], [name],
                 [Types.Opt(Types.Record({"name": Types.Text, "btcBalance": Types.Nat, "loan": Types.Nat}))])[0]
    return None if res is None else {"name": res["name"], "btcBalance": int(res["btcBalance"]), "loan": int(res["loan"])}

def get_all_users() -> List[Dict]:
    res = _query("getAllUsers", [], [],
                 [Types.Vec(Types.Record({"name": Types.Text, "btcBalance": Types.Nat, "loan": Types.Nat}))])[0]
    return [{"name": u["name"], "btcBalance": int(u["btcBalance"]), "loan": int(u["loan"])} for u in res]
