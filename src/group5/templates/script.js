const API_URL = "http://localhost:3000/spellcheck";

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

function displayWrongWords(wrongWords) {
    sidebar.innerHTML = "<h3>غلط های پیدا شده</h3>";

    wrongWords.forEach((wordObj, index) => {
        // Create a card for the word
        const card = document.createElement("div");
        card.className = "wrong-word-card";
        card.id = `wrong-word-card-${index}`; // Assign a unique ID to each card

        // Display the incorrect word
        const wordElement = document.createElement("h4");
        wordElement.textContent = wordObj[0]; // Incorrect word
        card.appendChild(wordElement);

        // Create buttons for suggestions
        const buttonContainer = document.createElement("div");
        buttonContainer.className = "button-container";

        wordObj[1].forEach((suggestion) => {
            const button = document.createElement("button");
            button.textContent = suggestion; // Suggestion text
            button.className = "card-button";
            button.addEventListener("click", () => {
                replaceWordInInput(wordObj[0], suggestion, `wrong-word-card-${index}`);
            });
            buttonContainer.appendChild(button);
        });

        card.appendChild(buttonContainer);
        sidebar.appendChild(card);
    });
}

function replaceWordInInput(oldWord, newWord, cardId) {
    // Replace the word in the text
    const text = inputText.value;
    const updatedText = text.split(' ').map(word => word === oldWord ? newWord : word).join(' ');
    inputText.value = updatedText;

    // Remove the card from the sidebar
    const card = document.getElementById(cardId);
    if (card) {
        card.remove();
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = inputText.value.trim();

    if (!text) {
        alert("لطفا متنی وارد کنید!");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error("خطا در ارتباط با سرور");
        }

        const result = await response.json();

        if (result && result.wrongWords && result.wrongWords.length > 0) {
            displayWrongWords(result.wrongWords);
        } else {
            sidebar.innerHTML = "<p>هیچ کلمه اشتباهی یافت نشد.</p>";
        }
    } catch (error) {
        console.error("Error:", error);
        sidebar.innerHTML = "<p>خطا در دریافت پاسخ از سرور.</p>";
    }
});