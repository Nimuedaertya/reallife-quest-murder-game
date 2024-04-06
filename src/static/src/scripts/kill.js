const killButton = document.getElementById("kill");
let ktimer = 10;
const kcountdown = document.getElementById("killcount");
let kcooldown = false;
const url  = window.location.href.split('/'); 
const user = url[url.length-1];
let timeStamp = Date.now();

function getKTimer(){
    $.ajax({ 
        url: '/getTimer/',
        type: 'POST', 
        success: function(response) { 
            response = JSON.parse(response);
            ktimer = response['kTimer'];
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
}


function getData(){
    $.ajax({ 
       url: '/kill/' + user, 
       type: 'POST', 
       success: function(response) { 
            response = JSON.parse(response);
            kcooldown = response['going'];
            if (kcooldown){
                timeStamp = response['timeStamp'];
                kWait();
            }
            else{
                killButton.disabled = false;
            }
       }, 
       error: function(error) { 
           console.log(error); 
       } 
   }); 
}

function sendTimer(bool, stamp){
    $.ajax({ 
       url: '/killTime/' + user, 
       type: 'POST', 
       data: {'going': bool, 'timeStamp': stamp},
       dataType: 'json',
       success: function(response) { 
       }, 
       error: function(error) { 
       } 
   }); 
   
}

function kCount(ktimeStamp){
    ktimeStamp = Number(ktimeStamp);
    kcooldown = true;
    sendTimer(kcooldown, ktimeStamp);
    ktimeStamp = Math.floor(ktimeStamp / 1000);
    let kcounter = ktimeStamp + ktimer;
    let kcountFn = setInterval(function () {
        ktimeStamp = kcounter - Math.floor(Date.now()/1000);
        kcountdown.innerText = "In " + ktimeStamp + " Sekunden wieder bereit.";
        if (ktimeStamp <= -1){
            clearInterval(kcountFn);
            kcountdown.classList.add("hidden");
            kcountdown.innerText = "";
            killButton.disabled = false;
            killButton.classList.remove("pause");
            killButton.classList.add("ready");
            kcooldown = false;
            sendTimer(false, '');
        }
    }, 1000);
}

function kWait(){
    if(killButton){
            killButton.classList.remove("ready");
            killButton.disabled = true;
            killButton.classList.add("pause");
            kcountdown.classList.remove("hidden");
            if(kcooldown){
                kCount(timeStamp);
            }
            else{
                console.log(Date.now());
                kCount(Date.now());
            }
    } 
}

if(killButton){
    killButton.disabled = true;
    getKTimer();
    getData();
    killButton.addEventListener("click", kWait);
}
