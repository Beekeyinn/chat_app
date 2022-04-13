document.querySelector("#room-name").focus();
document.querySelector("#room-name").onkeyup = (event) => {
  event.preventDefault();
  if (event.keyCode === 13) {
    document.querySelector("#submit").click();
  }
};

document.querySelector("#submit").onclick = (event) => {
  event.preventDefault();
  let roomname = document.querySelector("#room-name").value;
  window.location.pathname = "/chat/" + roomname + "/";
};
