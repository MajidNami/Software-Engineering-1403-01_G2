const TEXT_UPLOAD_URL = "http://localhost:8000/group5/text/";
const FILE_UPLOAD_URL = "http://localhost:8000/group5/file/";

const form = document.getElementById("textForm");
const inputText = document.getElementById("inputText");
const sidebar = document.getElementById("sidebar");
const addFileButton = document.getElementById("addFileButton");
const fileInput = document.createElement("input");

fileInput.type = "file";
fileInput.style.display = "none";
document.body.appendChild(fileInput);

const addFileButtonIcon = document.createElement("i");
addFileButtonIcon.className = "fa-solid fa-file";
addFileButton.appendChild(addFileButtonIcon);


addFileButton.addEventListener("click", () => {
    fileInput.click(); // open file selector
});

fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    inputText.disabled = true;
    addFileButtonIcon.className = "fas fa-spinner fa-pulse";

    try {
        const fileText = await file.text();
        inputText.value = fileText;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(FILE_UPLOAD_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("خطا در ارسال فایل");
        }

        const result = await response.json();

        if (result.wrongWords && result.wrongWords.length > 0) {
            displayWrongWords(result.wrongWords);
        } else {
            sidebar.innerHTML = "<p>هیچ کلمه اشتباهی یافت نشد.</p>";
        }
    } catch (error) {
        console.error("خطا:", error);
        alert("ارسال فایل با خطا مواجه شد.");
    } finally {
        addFileButtonIcon.className = "fa-solid fa-file";
        inputText.disabled = false;
        fileInput.value = "";
    }
});

inputText.focus();

inputText.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.shiftKey) {
        return;
    }
    if (e.key === "Enter") {
        e.preventDefault();
        form.dispatchEvent(new Event("submit"));
    }
});

function displayWrongWords(wrongWords) {
    sidebar.innerHTML = "<h3>غلط های پیدا شده</h3>";

     wrongWords.forEach((wordObj, index) => {
        const card = document.createElement("div");
        card.className = "wrong-word-card";
        card.id = `wrong-word-card-${index}`;

        const wordElement = document.createElement("h4");
        wordElement.textContent = wordObj.wrongWord || wordObj[0];
        card.appendChild(wordElement);

        const buttonContainer = document.createElement("div");
        buttonContainer.className = "button-container";

        const suggestions = wordObj.suggestions || wordObj[1];
        suggestions.forEach((suggestion) => {
            const button = document.createElement("button");
            button.textContent = suggestion;
            button.className = "card-button";
            button.addEventListener("click", () => {
                replaceWordInInput(wordObj.wrongWord || wordObj[0], suggestion, `wrong-word-card-${index}`);
            });
            buttonContainer.appendChild(button);
        });

        card.appendChild(buttonContainer);
        sidebar.appendChild(card);
    });
}

function replaceWordInInput(oldWord, newWord, cardId) {
    let text = inputText.value;
    const regex = new RegExp(oldWord, 'g');
    const updatedText = text.replace(regex, newWord);
    inputText.value = updatedText;
    const specificCard = document.getElementById(cardId);
    if (specificCard) {
        specificCard.remove();
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
        const response = await fetch(TEXT_UPLOAD_URL, {
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