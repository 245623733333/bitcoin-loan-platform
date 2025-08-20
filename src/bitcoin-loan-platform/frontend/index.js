import { HttpAgent, Actor } from "@dfinity/agent";
import { idlFactory as backendIDL } from "../../.dfx/local/canisters/bitcoin-loan-backend-backend";
const canisterId = "bkyz2-fmaaa-aaaaa-qaaaq-cai"; // Replace if needed

const agent = new HttpAgent();
const backend = Actor.createActor(backendIDL, {
  agent,
  canisterId,
});

document.getElementById("registerBtn").addEventListener("click", async () => {
  const name = document.getElementById("name").value;
  if (!name) return alert("Name is required");

  const result = await backend.registerUser(name);
  alert(result);
});
