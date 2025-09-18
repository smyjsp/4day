const form = document.getElementById("signupForm");
const emailInput = document.querySelector("input[name='email']");
const errorMessage = document.getElementById("errorMessage");

form.addEventListener("submit", (e) => {
    const email = emailInput.value;

    if (!(email.endsWith(".com") || email.endsWith(".mil") || email.endsWith(".edu"))) {
        e.preventDefault(); // stops form submission
        errorMessage.textContent = "Email must end with .com or .mil";
        errorMessage.style.color = "#317292";
    } else {
        errorMessage.textContent = "";
    }
});