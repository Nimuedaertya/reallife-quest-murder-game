// Create Websocket connection
const reportBtn = document.getElementById("report");
const img = "/static/src/images/AmongUsFavIcon.ico";

var socket = io();
socket.on("connect", function () {
  socket.emit("my event", { data: "I'm connected!" });
});

function report() {
  socket.emit("report", { data: "Alaaaarm!" });
}

// The Notification all player get on the report
function notificateRep() {
  new Notification("Alaaaarm!", {
    body: "Eine Leiche wurde gefunden!",
    icon: img,
    vibrate: [200, 100, 200],
  });
  console.log("Received");
}

socket.addEventListener("report", notificateRep);

if (reportBtn) {
  reportBtn.addEventListener("click", report);
}
