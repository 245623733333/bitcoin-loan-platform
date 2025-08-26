from loan_agent import loan_agent

# Save LoanAgent address for client use
with open("agent_address.txt", "w") as f:
    f.write(loan_agent.address)

print(f"LoanAgent running at: {loan_agent.address}")
loan_agent.run()
