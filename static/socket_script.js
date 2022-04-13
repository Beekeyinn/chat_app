const room_name = JSON.parse(document.getElementById("room-name").textContent);
const chatData = document.querySelector("#chat-data");
const logged_user_id = JSON.parse(
  document.getElementById("user-id").textContent
);
const chatContainer = document.querySelector(".chat-wrapper");

const scrollChatContainer = () => {
  if (chatContainer.clientHeight < chatContainer.scrollHeight) {
    chatContainer.scrollBy(0, chatContainer.scrollHeight);
  }
};

if (!chatData.hasChildNodes()) {
  const emptyText = document.createElement("h1");
  emptyText.id = "empty-text";
  emptyText.className = "empty-text";
  emptyText.innerText = "No Messages";
  chatData.appendChild(emptyText);
}

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + room_name + "/"
);

chatSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const user = data.user;
  const message = data.message;
  console.log("data", data);
  console.log("user", user);
  console.log("message", message.message);
  const messageElement = document.createElement("span");
  messageElement.innerText = message.message;
  messageElement.className = "message";

  const sendDate = new Date(message.send_at);
  console.log(sendDate);

  // user name span
  const userElement = document.createElement("span");
  userElement.innerText = message.send_by;
  userElement.className = "message-user";
  userElement.classList.add("hidden");

  // to show user who sent message
  messageElement.appendChild(userElement);

  if (document.querySelector("#empty-text")) {
    chatData.removeChild(document.querySelector("#empty-text"));
  }
  if (logged_user_id == user.id) {
    messageElement.classList.add("sender");
  } else {
    messageElement.classList.add("receiver");
  }

  chatData.appendChild(messageElement);
  scrollChatContainer();
};

chatSocket.onclose = function (event) {
  console.error("Chat socket closed unexpectedly");
};

document.querySelector("#chat-input").focus();
document.querySelector("#chat-input").onkeyup = function (event) {
  if (event.keyCode === 13) {
    document.querySelector("#send-msg").click();
  }
};

document.querySelector("#send-msg").onclick = function (event) {
  event.preventDefault();
  const msgInput = document.querySelector("#chat-input");
  const msg = msgInput.value;
  if (msg !== "") {
    chatSocket.send(
      JSON.stringify({
        message: msg,
      })
    );
  }
  msgInput.value = "";
};
