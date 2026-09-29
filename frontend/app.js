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

const API_URL = "http://127.0.0.1:8000";

let recognition = null;
let isListening = false;
let isTypingResponse = false;


function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text ?? "";
    return div.innerHTML;
}


function scrollToLatest(behavior = "smooth") {
    requestAnimationFrame(() => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: behavior
        });

        window.scrollTo({
            top: document.documentElement.scrollHeight,
            behavior: behavior
        });
    });
}


function addMessage(content, sender = "bot") {

    const message = document.createElement("div");

    if (sender === "user") {
        message.className = "message user-message";
    } else {
        message.className = "message bot-message";
    }


    const label = document.createElement("div");

    label.className = "message-label";

    label.textContent =
        sender === "user"
            ? "You"
            : "BharatYatraLM";


    const messageText =
        document.createElement("div");

    messageText.className =
        "message-text";

    messageText.innerHTML =
        content;


    message.appendChild(label);
    message.appendChild(messageText);

    chatMessages.appendChild(message);

    scrollToLatest();

    return messageText;
}


function addUserMessage(text) {

    if (emptyState) {
        emptyState.style.display = "none";
    }

    addMessage(
        escapeHtml(text),
        "user"
    );

    scrollToLatest();
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


    const bubble =
        document.createElement("div");

    bubble.className =
        "typing";


    bubble.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;


    message.appendChild(label);
    message.appendChild(bubble);

    chatMessages.appendChild(message);

    scrollToLatest();
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


function typeResponse(element, html) {

    return new Promise(resolve => {

        isTypingResponse = true;

        const temp =
            document.createElement("div");

        temp.innerHTML = html;


        const nodes =
            Array.from(temp.childNodes);


        element.innerHTML = "";

        let nodeIndex = 0;


        function processNode() {

            if (nodeIndex >= nodes.length) {

                isTypingResponse = false;

                scrollToLatest();

                resolve();

                return;
            }


            const originalNode =
                nodes[nodeIndex];


            if (
                originalNode.nodeType ===
                Node.TEXT_NODE
            ) {

                typeTextNode(
                    element,
                    originalNode.textContent,
                    () => {
                        nodeIndex++;
                        processNode();
                    }
                );

            } else {

                const newElement =
                    document.createElement(
                        originalNode.nodeName
                    );


                Array.from(
                    originalNode.attributes || []
                ).forEach(attribute => {

                    newElement.setAttribute(
                        attribute.name,
                        attribute.value
                    );
                });


                element.appendChild(
                    newElement
                );


                typeElementContents(
                    newElement,
                    originalNode,
                    () => {
                        nodeIndex++;
                        processNode();
                    }
                );
            }
        }


        processNode();
    });
}


function typeElementContents(
    target,
    source,
    callback
) {

    const children =
        Array.from(source.childNodes);


    if (children.length === 0) {

        callback();

        return;
    }


    let index = 0;


    function processChild() {

        if (index >= children.length) {

            callback();

            return;
        }


        const child =
            children[index];


        if (
            child.nodeType ===
            Node.TEXT_NODE
        ) {

            typeTextNode(
                target,
                child.textContent,
                () => {

                    index++;

                    processChild();
                }
            );

        } else {

            const newElement =
                document.createElement(
                    child.nodeName
                );


            Array.from(
                child.attributes || []
            ).forEach(attribute => {

                newElement.setAttribute(
                    attribute.name,
                    attribute.value
                );
            });


            target.appendChild(
                newElement
            );


            typeElementContents(
                newElement,
                child,
                () => {

                    index++;

                    processChild();
                }
            );
        }
    }


    processChild();
}


function typeTextNode(
    target,
    text,
    callback
) {

    const words =
        text.split(/(\s+)/);


    let index = 0;


    function addNextWord() {

        if (index >= words.length) {

            callback();

            return;
        }


        target.appendChild(
            document.createTextNode(
                words[index]
            )
        );


        index++;


        scrollToLatest("auto");


        setTimeout(
            addNextWord,
            35
        );
    }


    addNextWord();
}


function formatItinerary(data) {

    if (!data) {
        return "I couldn't generate an itinerary.";
    }


    let html = `
        <div class="response-title">
            ${escapeHtml(data.destination || "")} itinerary
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


    if (data.ideal_days !== undefined) {

        html += `
            <div class="response-info">
                Ideal duration:
                ${data.ideal_days} days
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
                        ${escapeHtml(day.day || "")}
                    </div>

                    <div class="itinerary-reason">
                        ${escapeHtml(day.reason || "")}
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


    if (data.results.length === 0) {

        return "I couldn't find nearby destinations within the requested radius.";
    }


    let html = `
        <div class="response-title">
            Nearby destinations around
            ${escapeHtml(data.destination || "")}
        </div>

        <div class="nearby-list">
    `;


    data.results.forEach(place => {

        const distance =
            Number(place.distance_km);


        html += `
            <div class="nearby-item">

                <div class="nearby-name">
                    ${escapeHtml(
                        place.destination_name || ""
                    )}
                </div>

                <div class="nearby-distance">
                    ${
                        Number.isFinite(distance)
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
                            place.destination_name || ""
                        )}
                    </div>

                    <div class="recommendation-details">
                        Trip:
                        ${place.ideal_trip_days ?? "N/A"} days
                        · Safety:
                        ${place.safety_rating ?? "N/A"}/10
                    </div>

                    <div class="recommendation-explanation">
                        ${escapeHtml(
                            place.explanation || ""
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
        return escapeHtml(message);
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


    if (intent === "itinerary") {

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


    if (intent === "nearby") {

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


    if (intent === "recommendation") {

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

    if (isTypingResponse) {
        return;
    }


    const message =
        chatInput.value.trim();


    if (!message) {
        return;
    }


    addUserMessage(message);

    chatInput.value = "";

    showTyping();

    sendButton.disabled = true;


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
                        message: message
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


        const messageElement =
            addMessage(
                "",
                "bot"
            );


        const formattedResponse =
            formatResponse(data);


        await typeResponse(
            messageElement,
            formattedResponse
        );


    } catch (error) {

        removeTyping();


        addMessage(
            "I couldn't connect to BharatYatraLM. Please make sure the FastAPI server is running.",
            "bot"
        );


        console.error(error);


    } finally {

        sendButton.disabled = false;

        chatInput.focus();
    }
}


function startNewChat() {

    chatMessages.innerHTML = "";

    if (emptyState) {
        emptyState.style.display = "";
    }

    chatInput.value = "";

    chatInput.focus();

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

                const text =
                    prompt.textContent.trim();

                chatInput.value =
                    text;

                sendMessage();
            }
        );
    });
}


function setupVoiceRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        voiceButton.addEventListener(
            "click",
            () => {

                addMessage(
                    "Voice input is not supported by this browser. Please use Chrome or another browser with Speech Recognition support.",
                    "bot"
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


    recognition.onstart = () => {

        isListening = true;

        voiceButton.classList.add(
            "listening"
        );


        if (voiceStatus) {

            voiceStatus.textContent =
                "Listening...";

            voiceStatus.classList.add(
                "active"
            );
        }
    };


    recognition.onresult =
        event => {

            let transcript = "";


            for (
                let i = event.resultIndex;
                i < event.results.length;
                i++
            ) {

                transcript +=
                    event.results[i][0]
                        .transcript;
            }


            chatInput.value =
                transcript;
        };


    recognition.onend = () => {

        isListening = false;

        voiceButton.classList.remove(
            "listening"
        );


        if (voiceStatus) {

            voiceStatus.textContent =
                "";

            voiceStatus.classList.remove(
                "active"
            );
        }
    };


    recognition.onerror =
        error => {

            console.error(error);

            isListening = false;

            voiceButton.classList.remove(
                "listening"
            );


            if (voiceStatus) {

                voiceStatus.textContent =
                    "";

                voiceStatus.classList.remove(
                    "active"
                );
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


    if (savedTheme === "dark") {

        document.body.classList.add(
            "dark-mode"
        );
    }


    updateThemeButton();


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


function setupSplashScreen() {

    window.addEventListener(
        "load",
        () => {

            setTimeout(
                () => {

                    if (splashScreen) {

                        splashScreen.classList.add(
                            "hide"
                        );
                    }

                },
                700
            );
        }
    );
}


sendButton.addEventListener(
    "click",
    sendMessage
);


chatInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


newChatButton.addEventListener(
    "click",
    startNewChat
);


attachExamplePromptEvents();

setupVoiceRecognition();

setupTheme();

setupSplashScreen();