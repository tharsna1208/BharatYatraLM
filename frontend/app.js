const API_URL = "http://127.0.0.1:8000";

const splashScreen = document.getElementById("splashScreen");
const emptyState = document.getElementById("emptyState");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const voiceButton = document.getElementById("voiceButton");
const voiceIcon = document.getElementById("voiceIcon");
const voiceStatus = document.getElementById("voiceStatus");
const chatMessages = document.getElementById("chatMessages");
const newChatButton = document.getElementById("newChatButton");
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeText = document.getElementById("themeText");
const examplePrompts = document.querySelectorAll(".example-prompt");

let hasMessages = false;
let recognition = null;
let isListening = false;


function setMicrophoneIcon() {

    voiceIcon.innerHTML = `
        <path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3Z"></path>
        <path d="M19 11a7 7 0 0 1-14 0"></path>
        <path d="M12 18v4"></path>
        <path d="M8 22h8"></path>
    `;

}


function setStopIcon() {

    voiceIcon.innerHTML = `
        <path d="M7 7h10v10H7z"></path>
    `;

}


function applyTheme(theme) {

    if (theme === "dark") {

        document.body.classList.add("dark-mode");

        themeIcon.textContent = "☀";

        themeText.textContent = "Light Mode";

    } else {

        document.body.classList.remove("dark-mode");

        themeIcon.textContent = "☾";

        themeText.textContent = "Dark Mode";

    }

    localStorage.setItem(
        "bharatYatraTheme",
        theme
    );

}


function loadTheme() {

    const savedTheme =
        localStorage.getItem(
            "bharatYatraTheme"
        );

    if (savedTheme) {

        applyTheme(savedTheme);

    } else {

        applyTheme("light");

    }

}


loadTheme();


themeToggle.addEventListener(
    "click",
    () => {

        const isDark =
            document.body.classList.contains(
                "dark-mode"
            );

        applyTheme(
            isDark
                ? "light"
                : "dark"
        );

    }
);


window.addEventListener(
    "load",
    () => {

        setTimeout(
            () => {

                splashScreen.classList.add(
                    "hide"
                );

                userInput.focus();

            },
            700
        );

    }
);


function addMessage(
    message,
    type
) {

    const messageContainer =
        document.createElement(
            "div"
        );

    messageContainer.classList.add(
        "message",
        type === "user"
            ? "user-message"
            : "bot-message"
    );


    const label =
        document.createElement(
            "div"
        );

    label.classList.add(
        "message-label"
    );

    label.textContent =
        type === "user"
            ? "You"
            : "BharatYatraLM";


    const text =
        document.createElement(
            "div"
        );

    text.classList.add(
        "message-text"
    );

    text.textContent =
        message;


    messageContainer.appendChild(
        label
    );

    messageContainer.appendChild(
        text
    );

    chatMessages.appendChild(
        messageContainer
    );


    messageContainer.scrollIntoView(
        {
            behavior: "smooth",
            block: "nearest"
        }
    );

}


function showChat() {

    if (!hasMessages) {

        hasMessages = true;

        emptyState.style.display =
            "none";

    }

}


function setLoading(
    isLoading
) {

    sendButton.disabled =
        isLoading;

    if (isLoading) {

        sendButton.textContent =
            "⋯";

    } else {

        sendButton.textContent =
            "↑";

    }

}


async function sendMessage(
    message = null
) {

    const text =
        message !== null
            ? message.trim()
            : userInput.value.trim();


    if (!text) {

        return;

    }


    if (isListening) {

        stopVoiceRecognition();

    }


    showChat();


    addMessage(
        text,
        "user"
    );


    userInput.value = "";

    userInput.style.height =
        "auto";


    setLoading(true);


    try {

        const response =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            message: text
                        }
                    )
                }
            );


        if (!response.ok) {

            throw new Error(
                "API request failed"
            );

        }


        const data =
            await response.json();


        addMessage(
            data.answer ||
            "I could not find a suitable answer.",
            "bot"
        );


    } catch (error) {

        addMessage(
            "I couldn't connect to BharatYatraLM. Please make sure the FastAPI server is running.",
            "bot"
        );

    } finally {

        setLoading(false);

        userInput.focus();

    }

}


function setupVoiceRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        voiceButton.addEventListener(
            "click",
            () => {

                voiceStatus.textContent =
                    "Voice input is not supported in this browser.";

                voiceStatus.classList.add(
                    "active"
                );

                setTimeout(
                    () => {

                        voiceStatus.classList.remove(
                            "active"
                        );

                    },
                    3000
                );

            }
        );

        return;

    }


    recognition =
        new SpeechRecognition();


    recognition.continuous =
        false;

    recognition.interimResults =
        true;

    recognition.lang =
        "en-IN";


    recognition.onstart =
        () => {

            isListening =
                true;

            voiceButton.classList.add(
                "listening"
            );

            setStopIcon();

            voiceStatus.textContent =
                "Listening...";

            voiceStatus.classList.add(
                "active"
            );

        };


    recognition.onresult =
        (event) => {

            let transcript =
                "";

            for (
                let i = event.resultIndex;
                i < event.results.length;
                i++
            ) {

                transcript +=
                    event.results[i][0].transcript;

            }


            userInput.value =
                transcript;

            userInput.style.height =
                "auto";

            userInput.style.height =
                Math.min(
                    userInput.scrollHeight,
                    130
                ) + "px";

        };


    recognition.onerror =
        (event) => {

            if (
                event.error ===
                "not-allowed"
            ) {

                voiceStatus.textContent =
                    "Microphone permission was denied.";

            } else if (
                event.error ===
                "no-speech"
            ) {

                voiceStatus.textContent =
                    "I didn't hear anything.";

            } else {

                voiceStatus.textContent =
                    "Voice input stopped.";

            }

            voiceStatus.classList.add(
                "active"
            );

        };


    recognition.onend =
        () => {

            isListening =
                false;

            voiceButton.classList.remove(
                "listening"
            );

            setMicrophoneIcon();

            setTimeout(
                () => {

                    voiceStatus.classList.remove(
                        "active"
                    );

                },
                1800
            );

        };

}


function startVoiceRecognition() {

    if (!recognition) {

        return;

    }


    if (isListening) {

        stopVoiceRecognition();

        return;

    }


    try {

        recognition.start();

    } catch (error) {

        stopVoiceRecognition();

    }

}


function stopVoiceRecognition() {

    if (
        recognition &&
        isListening
    ) {

        recognition.stop();

    }

}


setupVoiceRecognition();


voiceButton.addEventListener(
    "click",
    () => {

        startVoiceRecognition();

    }
);


sendButton.addEventListener(
    "click",
    () => {

        sendMessage();

    }
);


userInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


userInput.addEventListener(
    "input",
    () => {

        userInput.style.height =
            "auto";

        userInput.style.height =
            Math.min(
                userInput.scrollHeight,
                130
            ) + "px";

    }
);


examplePrompts.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                const label =
                    button.querySelector(
                        "span"
                    );

                const question =
                    button.textContent
                        .replace(
                            label
                                ? label.textContent
                                : "",
                            ""
                        )
                        .trim();

                sendMessage(
                    question
                );

            }
        );

    }
);


newChatButton.addEventListener(
    "click",
    () => {

        if (isListening) {

            stopVoiceRecognition();

        }


        chatMessages.innerHTML =
            "";

        hasMessages =
            false;

        emptyState.style.display =
            "block";

        userInput.value =
            "";

        userInput.style.height =
            "auto";

        userInput.focus();

    }
);