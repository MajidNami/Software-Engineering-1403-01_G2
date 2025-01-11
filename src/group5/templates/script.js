const API_URL = "http://example/spellcheck";

const form = document.getElementById("textForm");
const inputText = document.getElementById("inputText");
const sidebar = document.getElementById("sidebar");

// Set focus on the input field by default
inputText.focus();

// Event to submit the form using the Enter key
inputText.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.shiftKey) {
        return; // Create a new line (default browser behavior)
    }
    if (e.key === "Enter") { // If the Enter key is pressed
        e.preventDefault(); // Prevent creating a new line
        form.dispatchEvent(new Event("submit")); // Programmatically submit the form
    }
});