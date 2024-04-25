notiPlace = document.getElementById("noti");

function askNotificationPermission() {
  // Check if the browser supports notifications
  if (!("Notification" in window)) {
    console.log("This browser does not support notifications.");
    return;
  }
}
const notibtn = document.createElement("button");
notibtn.textContent = "Notifications erlauben";
notiPlace.append(notibtn);

function rePer() {
  Notification.requestPermission();
  if (Notification.permission == "granted") {
    notiPlace?.removeChild(notiPlace.lastChild);
  }
}

if (notibtn) {
  notibtn.addEventListener("click", rePer);
}

if (Notification.permission == "granted") {
  notiPlace?.removeChild(notiPlace.lastChild);
}
