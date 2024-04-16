const notificationBtn = document.getElementById("enable");

function askNotificationPermission() {
  // Check if the browser supports notifications
  if (!("Notification" in window)) {
    console.log("This browser does not support notifications.");
    return;
  }
  Notification.requestPermission().then((permission) => {
    // set the button to shown or hidden, depending on what the user answers
    notificationBtn.style.display = permission === "granted" ? "none" : "block";
  });
}

if (notificationBtn) {
  notificationBtn.addEventListener("click", askNotificationPermission);
}

if (notificationBtn && Notification.permission == "granted") {
  notificationBtn.style.display = "none";
}
