const message = document.getElementById("msg");

setTimeout(() => {
  if (message) {
    message.remove();
  }
}, 2000);
