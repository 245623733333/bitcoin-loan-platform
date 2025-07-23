# 💰 Bitcoin-Backed Loan Platform

A next-generation DeFi lending platform powered by the **Internet Computer Protocol (ICP)** that enables users to unlock liquidity without selling their Bitcoin. This project uses non-custodial smart contracts for secure, decentralized loan issuance.

## 🌐 Live Project

📎 [Frontend Hosted on GitHub Pages](https://245623733333.github.io/bitcoin-loan-platform/)

> **Note:** This is the frontend UI only. Backend logic and Bitcoin integration run locally using `dfx`.

## 🧩 Canister Architecture (Local Development)

- **Frontend Canister ID**: `u6s2n-gx777-77774-qaaba-cai`
- **Backend Canister ID**: `uxrrr-q7777-77774-qaaaq-cai`
- **Local DApp URL**:  
  `http://127.0.0.1:4943/?canisterId=u6s2n-gx777-77774-qaaba-cai&id=uxrrr-q7777-77774-qaaaq-cai`

---

## 🚀 Features

- 🔐 **Trustless Bitcoin Collateralization**
- ⚡ **Instant, Non-Custodial Loans**
- 🌍 **Global Access with No Credit Checks**
- 🔎 **Smart Contracts Auditable On-Chain**
- 🛠️ **Built Using Motoko + ICP + HTML/CSS**

---

## 🗂️ Project Structure

```bash
bitcoin-loan-platform/
│
├── backend/
│   └── bitcoin-loan-backend-backend/
│       └── main.mo          # Motoko smart contract
│
├── frontend/
│   └── index.html           # User interface
│
├── dfx.json                 # ICP canister configuration
├── README.md                # Project overview
└── .gitignore               # Git ignored files
