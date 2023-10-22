
function generate(){
    var characters = ["cinna_teacup.png", "hello_kitty.png", "kuromi.png", "melody.png", "pompom.png"];
    var num = Math.floor(Math.random() * characters.length) //Math.random generates a random number between 0 and 1
    var char = document.getElementById("chosen")
    console.log(characters.length)
    console.log(num)
    char.style.visibility = "hidden"
    char.src = "/image/" + characters[num]
    char.style.visibility = "visible"
}

//Literally copy + paste from HW 2 functions.js
function deleteMessage(messageId) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    console.log(messageID)
    request.open("DELETE", "/chat-message/" + messageId);
    request.send();
}

function chatMessageHTML(messageJSON) {
    console.log(messageJSON)
    const username = messageJSON.username;
    const message = messageJSON.message;
    const messageId = messageJSON.id;
    const messageTitle = messageJSON.title;
    const likes = messageJSON.likes; // Turns the number of likes from message.JSON to number of likes
    // Line below creates the HTML post in article format.
    let messageHTML = "" +
        "<article id = 'message_" + messageId +"'>" +
        "<h1>" + messageTitle + "</h1>" +
        "<h3>" + username + "</h3>" +
        "<p>" + message + "</p>" +
        "<p><button onclick='deleteMessage(\"" + messageId + "\")' id='heart'>❤️</button></p>" +
        "<p>" + likes + ' likes' + "</p>" +
        "</article>";
    // let messageHTML = "<br><button onclick='deleteMessage(\"" + messageId + "\")'>X</button> ";
    //messageHTML += "<span id='message_" + messageId + "'>" + "<b>" + username + "</b>: " + message + "</span>";
    return messageHTML;
}

function clearChat() {
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML = "";
}

function addMessageToChat(messageJSON) {
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML += chatMessageHTML(messageJSON);
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function sendChat() {
    const chatTitle = document.getElementById("title-box");
    const chatTextBox = document.getElementById("chat-text-box");
    const title = chatTitle.value;
    const message = chatTextBox.value;
    chatTitle.value = "";
    chatTextBox.value = "";
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }

    //Insert the xsrf token in the chat (hidden) by replacing its value in the HTML
    const xsrf = document.getElementById("xsrf");
    const messageJSON = {"title": title, "message": message, "xsrf": xsrf.value };
    request.open("POST", "/chat-message");
    request.send(JSON.stringify(messageJSON));
    chatTextBox.focus();
}

function updateChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearChat();
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessageToChat(message);
            }
        }
    }
    request.open("GET", "/chat-history");
    request.send();
}

function welcome() {
    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendChat();
        }
    });
    
    console.log("got into the welcome page")
    document.getElementById("paragraph").innerHTML += "<br/>This text was added by JavaScript 😀";
    document.getElementById("chat-text-box").focus();
    document.getElementById("title-box").focus()

    updateChat();
    setInterval(updateChat, 2000);
}
