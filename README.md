# 💰 Bitcoin-Backed Loan Platform

A next-generation DeFi lending platform powered by the **Internet Computer Protocol (ICP)** that enables users to unlock liquidity without selling their Bitcoin. This project uses non-custodial smart contracts for secure, decentralized loan issuance.

The Bitcoin Loan Platform is a decentralized Web3 application built using the Internet Computer Protocol (ICP) and Fetch.ai agents.
It allows users to:

Register on-chain identities.

Deposit Bitcoin balances.

Request and manage loans.

Interact with the system using Fetch.ai Chat Protocol and ICP’s smart contract backend.

🚀 Features

ICP Smart Contract Backend (Motoko)

User registration

Deposit tracking

Loan requests and repayments

Persistent state management

Fetch.ai Agents

Chat-based interaction with the loan platform.

Handles off-chain logic and communication.

Registered under Innovation Lab.

Frontend Canister

Simple web UI for interaction.

🏗️ Architecture

High-Level Flow:

Users register and interact with the ICP backend.

Fetch.ai agent provides conversational UI via Chat Protocol.

Data is stored on-chain in the ICP canister.

[User] ↔ [Fetch.ai Agent] ↔ [ICP Canister Backend] ↔ [ICP Frontend]

🔧 Installation & Running Locally
Prerequisites

DFX SDK

Node.js (for frontend if expanded)

Fetch.ai agent tooling

Steps
# Clone repository
git clone https://github.com/<your-username>/bitcoin-loan-platform.git
cd bitcoin-loan-platform

# Start local replica
dfx start --background

# Deploy canisters
dfx deploy

# Call backend methods
dfx canister call bitcoin-loan-backend-backend registerUser '("Alice")'
dfx canister call bitcoin-loan-backend-backend deposit '("Alice", 50)'
dfx canister call bitcoin-loan-backend-backend takeLoan '("Alice", 100)'
dfx canister call bitcoin-loan-backend-backend getAllUsers

🌐 Local Canisters

Frontend Canister:
http://127.0.0.1:4943/?canisterId=be2us-64aaa-aaaaa-qaabq-cai

Backend Canister (Candid UI):
http://127.0.0.1:4943/?canisterId=bd3sg-teaaa-aaaaa-qaaba-cai&id=bkyz2-fmaaa-aaaaa-qaaaq-cai

📹 Demo Video

👉https://onedrive.live.com/?qt=allmyphotos&photosData=%2Fshare%2F664A206601A904D2%21s62e772e3e5d24a82b39d1a06965284c3%3Fithint%3Dvideo%26migratedtospo%3Dtrue&cid=664A206601A904D2&id=664A206601A904D2%21s62e772e3e5d24a82b39d1a06965284c3&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3YvYy82NjRhMjA2NjAxYTkwNGQyL0VlTnk1MkxTNVlKS3M1MGFCcFpTaE1NQlpLbFUwWUpzU1NZbzBFbGlUblJWUVE&v=photos

📝 Challenges Faced

Setting up Motoko backend with stable storage.

Integrating Fetch.ai Chat Protocol with ICP backend.

Debugging state persistence and testing multiple canisters.

🔮 Future Plans

Add loan repayment and interest calculation.

Improve frontend with React + ICP agent integration.

Deploy on ICP mainnet.

Expand Fetch.ai agent capabilities (e.g., credit scoring).


📂 Repo Structure
bitcoin-loan-platform/
├── backend/
│   └── bitcoin-loan-backend-backend/
│       └── main.mo        # ICP Motoko smart contract
├── src/
│   └── frontend/          # (Optional UI code)
├── dfx.json               # ICP config
├── README.md              # Project documentation
└── index.html             # Simple frontend entry
