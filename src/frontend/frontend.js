import { bitcoin_loan_backend } from "./declarations/bitcoin_loan_backend/index.js";
const registerBtn = document.getElementById("registerBtn");
const applyLoanBtn = document.getElementById("applyLoanBtn");
const usernameInput = document.getElementById("username");

registerBtn.addEventListener("click", async () => {
  const username = usernameInput.value;
  if (!username) return alert("Enter a username first!");
  try {
    const result = await bitcoin_loan_backend.registerUser(username);
    alert(result);
  } catch (err) {
    console.error(err);
    alert("Error registering user");
  }
});

applyLoanBtn.addEventListener("click", async () => {
  const username = usernameInput.value;
  if (!username) return alert("Enter a username first!");
  try {
    const result = await bitcoin_loan_backend.takeLoan(username, 100);
    alert(result);
  } catch (err) {
    console.error(err);
    alert("Error applying for loan");
  }
});
