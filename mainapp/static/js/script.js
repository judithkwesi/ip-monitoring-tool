const message = document.getElementById("msg");

setTimeout(() => {
  if (message) {
    message.remove();
  }
}, 2000);

document.getElementById("hamburger").addEventListener("click", function () {
  const menuLinks = document.getElementById("menu-links");
  if (menuLinks.style.display === "block") {
    menuLinks.style.display = "none";
  } else {
    menuLinks.style.display = "block";
  }
});
