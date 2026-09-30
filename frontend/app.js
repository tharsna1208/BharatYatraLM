const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const newChatButton = document.getElementById("newChatButton");
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeText = document.getElementById("themeText");
const voiceButton = document.getElementById("voiceButton");
const voiceStatus = document.getElementById("voiceStatus");
const emptyState = document.getElementById("emptyState");
const splashScreen = document.getElementById("splashScreen");
const mainApp = document.getElementById("mainApp");

const API_URL = "https://bharatyatralm.onrender.com";

let recognition = null;
let isListening = false;

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text ?? "";
    return div.innerHTML;
}

function scrollToMessage(message, smooth = true) {
    if (!message) {
        return;
    }

    message.scrollIntoView({
        behavior: smooth ? "smooth" : "auto",
        block: "center"
    });
}

function scrollToBottom() {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "smooth"
    });
}

function addUserMessage(text) {
    if (emptyState) {
        emptyState.style.display = "none";
    }

    const message = document.createElement("div");

    message.className =
        "message user-message";

    const label = document.createElement("div");

    label.className =
        "message-label";

    label.textContent =
        "You";

    const messageText =
        document.createElement("div");

    messageText.className =
        "message-text";

    messageText.textContent =
        text;

    message.appendChild(label);
    message.appendChild(messageText);

    chatMessages.appendChild(message);

    requestAnimationFrame(() => {
        scrollToMessage(message);
    });
}

function showTyping() {
    const message =
        document.createElement("div");

    message.className =
        "message bot-message";

    message.id =
        "typingMessage";

    const label =
        document.createElement("div");

    label.className =
        "message-label";

    label.textContent =
        "BharatYatraLM";

    const messageText =
        document.createElement("div");

    messageText.className =
        "message-text typing";

    messageText.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    message.appendChild(label);
    message.appendChild(messageText);

    chatMessages.appendChild(message);

    requestAnimationFrame(() => {
        scrollToMessage(message);
    });
}

function removeTyping() {
    const typingMessage =
        document.getElementById(
            "typingMessage"
        );

    if (typingMessage) {
        typingMessage.remove();
    }
}

function prepareAnimatedContent(content) {
    const container =
        document.createElement("div");

    container.innerHTML =
        content;

    const walker =
        document.createTreeWalker(
            container,
            NodeFilter.SHOW_TEXT
        );

    const textNodes = [];

    while (walker.nextNode()) {
        if (
            walker.currentNode.nodeValue.trim()
        ) {
            textNodes.push(
                walker.currentNode
            );
        }
    }

    const wordSpans = [];

    textNodes.forEach(node => {
        const text =
            node.nodeValue;

        const parts =
            text.split(/(\s+)/);

        const fragment =
            document.createDocumentFragment();

        parts.forEach(part => {
            if (/^\s+$/.test(part)) {
                fragment.appendChild(
                    document.createTextNode(
                        part
                    )
                );
            } else if (part) {
                const span =
                    document.createElement(
                        "span"
                    );

                span.textContent =
                    part;

                span.style.opacity =
                    "0";

                span.style.transition =
                    "opacity 0.12s ease";

                fragment.appendChild(
                    span
                );

                wordSpans.push(
                    span
                );
            }
        });

        node.parentNode.replaceChild(
            fragment,
            node
        );
    });

    return {
        container,
        wordSpans
    };
}

async function animateBotMessage(content) {
    const message =
        document.createElement("div");

    message.className =
        "message bot-message";

    const label =
        document.createElement("div");

    label.className =
        "message-label";

    label.textContent =
        "BharatYatraLM";

    const messageText =
        document.createElement("div");

    messageText.className =
        "message-text";

    const prepared =
        prepareAnimatedContent(
            content
        );

    messageText.appendChild(
        prepared.container
    );

    message.appendChild(
        label
    );

    message.appendChild(
        messageText
    );

    chatMessages.appendChild(
        message
    );

    requestAnimationFrame(() => {
        scrollToMessage(
            message,
            false
        );
    });

    let lastScroll = 0;

    for (
        let i = 0;
        i < prepared.wordSpans.length;
        i++
    ) {
        const word =
            prepared.wordSpans[i];

        word.style.opacity =
            "1";

        if (
            i === 0 ||
            i % 3 === 0 ||
            i ===
                prepared.wordSpans.length - 1
        ) {
            const now =
                Date.now();

            if (
                now - lastScroll >
                70
            ) {
                scrollToMessage(
                    message,
                    true
                );

                lastScroll =
                    now;
            }
        }

        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    28
                )
        );
    }

    scrollToMessage(
        message,
        true
    );
}

function formatItinerary(data) {
    if (!data) {
        return "I couldn't generate an itinerary.";
    }

    let html = `
        <div class="response-title">
            ${escapeHtml(
                data.destination || ""
            )} itinerary
        </div>
    `;

    if (
        data.minimum_days !== undefined &&
        data.maximum_days !== undefined
    ) {
        html += `
            <div class="response-info">
                Recommended duration:
                ${data.minimum_days}–${data.maximum_days} days
            </div>
        `;
    }

    if (
        Array.isArray(data.days) &&
        data.days.length > 0
    ) {
        html += `
            <div class="itinerary-list">
        `;

        data.days.forEach(day => {
            html += `
                <div class="itinerary-item">

                    <div class="itinerary-day">
                        ${escapeHtml(
                            day.day || ""
                        )}
                    </div>

                    <div class="itinerary-reason">
                        ${escapeHtml(
                            day.reason || ""
                        )}
                    </div>

                </div>
            `;
        });

        html += `
            </div>
        `;
    }

    return html;
}

function formatNearby(data) {
    if (
        !data ||
        !Array.isArray(data.results)
    ) {
        return "I couldn't find nearby destinations.";
    }

    if (
        data.results.length === 0
    ) {
        return "I couldn't find nearby destinations within the requested radius.";
    }

    let html = `
        <div class="response-title">
            Nearby destinations around
            ${escapeHtml(
                data.destination || ""
            )}
        </div>

        <div class="nearby-list">
    `;

    data.results.forEach(place => {
        const distance =
            Number(
                place.distance_km
            );

        html += `
            <div class="nearby-item">

                <div class="nearby-name">
                    ${escapeHtml(
                        place.destination_name ||
                        ""
                    )}
                </div>

                <div class="nearby-distance">
                    ${
                        Number.isFinite(
                            distance
                        )
                            ? distance.toFixed(1)
                            : "N/A"
                    } km away
                </div>

            </div>
        `;
    });

    html += `
        </div>
    `;

    return html;
}

function formatRecommendations(data) {
    if (
        !Array.isArray(data) ||
        data.length === 0
    ) {
        return "I couldn't find matching destinations.";
    }

    let html = `
        <div class="response-title">
            Destinations matching your preferences
        </div>

        <div class="recommendation-list">
    `;

    data.forEach((place, index) => {
        html += `
            <div class="recommendation-item">

                <div class="recommendation-rank">
                    ${index + 1}
                </div>

                <div class="recommendation-content">

                    <div class="recommendation-name">
                        ${escapeHtml(
                            place.destination_name ||
                            ""
                        )}
                    </div>

                    <div class="recommendation-details">
                        Trip:
                        ${
                            place.ideal_trip_days ??
                            "N/A"
                        } days
                        · Safety:
                        ${
                            place.safety_rating ??
                            "N/A"
                        }/10
                    </div>

                    <div class="recommendation-explanation">
                        ${escapeHtml(
                            place.explanation ||
                            ""
                        )}
                    </div>

                </div>

            </div>
        `;
    });

    html += `
        </div>
    `;

    return html;
}

function formatChat(data, message) {
    if (message) {
        return escapeHtml(
            message
        );
    }

    if (
        data &&
        data.answer
    ) {
        return escapeHtml(
            data.answer
        );
    }

    return "I couldn't generate a response.";
}

function formatResponse(response) {
    const intent =
        response.intent;

    const data =
        response.data;

    if (
        intent === "itinerary"
    ) {
        return `
            <div class="response-intro">
                ${escapeHtml(
                    response.message ||
                    "Here is your personalized itinerary."
                )}
            </div>

            ${formatItinerary(data)}
        `;
    }

    if (
        intent === "nearby"
    ) {
        return `
            <div class="response-intro">
                ${escapeHtml(
                    response.message ||
                    "Here are some nearby destinations."
                )}
            </div>

            ${formatNearby(data)}
        `;
    }

    if (
        intent === "recommendation"
    ) {
        return `
            <div class="response-intro">
                ${escapeHtml(
                    response.message ||
                    "Here are some destinations that match your preferences."
                )}
            </div>

            ${formatRecommendations(data)}
        `;
    }

    return formatChat(
        data,
        response.message
    );
}

async function sendMessage() {
    if (!chatInput) {
        return;
    }

    const message =
        chatInput.value.trim();

    if (!message) {
        return;
    }

    addUserMessage(
        message
    );

    chatInput.value =
        "";

    showTyping();

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

                    body: JSON.stringify({
                        message:
                            message
                    })
                }
            );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        removeTyping();

        const formatted =
            formatResponse(
                data
            );

        await animateBotMessage(
            formatted
        );

    } catch (error) {
        removeTyping();

        await animateBotMessage(
            "I couldn't connect to BharatYatraLM. Please try again in a moment."
        );

        console.error(
            "BharatYatraLM API error:",
            error
        );
    }
}

function startNewChat() {
    if (chatMessages) {
        chatMessages.innerHTML =
            "";
    }

    if (emptyState) {
        emptyState.style.display =
            "";
    }

    if (chatInput) {
        chatInput.value =
            "";

        chatInput.focus();
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function attachExamplePromptEvents() {
    const prompts =
        document.querySelectorAll(
            ".example-prompt"
        );

    prompts.forEach(prompt => {
        prompt.addEventListener(
            "click",
            () => {
                if (!chatInput) {
                    return;
                }

                chatInput.value =
                    prompt.textContent.trim();

                sendMessage();
            }
        );
    });
}

function setupVoiceRecognition() {
    if (!voiceButton) {
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        voiceButton.addEventListener(
            "click",
            () => {
                animateBotMessage(
                    "Voice input is not supported by this browser. Please use Chrome or another browser with Speech Recognition support."
                );
            }
        );

        return;
    }

    recognition =
        new SpeechRecognition();

    recognition.lang =
        "en-IN";

    recognition.continuous =
        false;

    recognition.interimResults =
        true;

    recognition.onstart =
        () => {
            isListening =
                true;

            voiceButton.classList.add(
                "listening"
            );

            if (voiceStatus) {
                voiceStatus.textContent =
                    "Listening...";
            }
        };

    recognition.onresult =
        event => {
            let transcript =
                "";

            for (
                let i =
                    event.resultIndex;
                i <
                    event.results.length;
                i++
            ) {
                transcript +=
                    event.results[i][0]
                        .transcript;
            }

            if (chatInput) {
                chatInput.value =
                    transcript;
            }
        };

    recognition.onend =
        () => {
            isListening =
                false;

            voiceButton.classList.remove(
                "listening"
            );

            if (voiceStatus) {
                voiceStatus.textContent =
                    "";
            }
        };

    recognition.onerror =
        error => {
            console.error(
                "Speech recognition error:",
                error
            );

            isListening =
                false;

            voiceButton.classList.remove(
                "listening"
            );

            if (voiceStatus) {
                voiceStatus.textContent =
                    "";
            }
        };

    voiceButton.addEventListener(
        "click",
        () => {
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }
    );
}

function updateThemeButton() {
    const darkModeEnabled =
        document.body.classList.contains(
            "dark-mode"
        );

    if (themeIcon) {
        themeIcon.textContent =
            darkModeEnabled
                ? "☀"
                : "☾";
    }

    if (themeText) {
        themeText.textContent =
            darkModeEnabled
                ? "Light Mode"
                : "Dark Mode";
    }
}

function setupTheme() {
    const savedTheme =
        localStorage.getItem(
            "bharatyatralm-theme"
        );

    if (
        savedTheme === "dark"
    ) {
        document.body.classList.add(
            "dark-mode"
        );
    }

    updateThemeButton();

    if (!themeToggle) {
        return;
    }

    themeToggle.addEventListener(
        "click",
        () => {
            document.body.classList.toggle(
                "dark-mode"
            );

            const darkModeEnabled =
                document.body.classList.contains(
                    "dark-mode"
                );

            localStorage.setItem(
                "bharatyatralm-theme",
                darkModeEnabled
                    ? "dark"
                    : "light"
            );

            updateThemeButton();
        }
    );
}

function hideSplashScreen() {
    if (splashScreen) {
        splashScreen.classList.add(
            "hide"
        );

        splashScreen.style.opacity =
            "0";

        splashScreen.style.visibility =
            "hidden";

        splashScreen.style.pointerEvents =
            "none";

        splashScreen.style.display =
            "none";
    }

    if (mainApp) {
        mainApp.classList.add(
            "visible"
        );

        mainApp.style.display =
            "flex";

        mainApp.style.opacity =
            "1";

        mainApp.style.visibility =
            "visible";
    }
}

function initializeBharatYatraLM() {
    if (sendButton) {
        sendButton.addEventListener(
            "click",
            sendMessage
        );
    }

    if (chatInput) {
        chatInput.addEventListener(
            "keydown",
            event => {
                if (
                    event.key ===
                        "Enter" &&
                    !event.shiftKey
                ) {
                    event.preventDefault();

                    sendMessage();
                }
            }
        );
    }

    if (newChatButton) {
        newChatButton.addEventListener(
            "click",
            startNewChat
        );
    }

    attachExamplePromptEvents();

    setupVoiceRecognition();

    setupTheme();

    setTimeout(
        hideSplashScreen,
        700
    );
}

if (
    document.readyState ===
    "loading"
) {
    document.addEventListener(
        "DOMContentLoaded",
        initializeBharatYatraLM
    );
} else {
    initializeBharatYatraLM();
}