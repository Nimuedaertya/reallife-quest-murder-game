const deadButton = document.getElementById("dead_button");
let dead = false;
const url_dead  = window.location.href.split('/'); 
const user_dead = url_dead[url_dead.length-1];

function getData(){
    $.ajax({ 
       url: '/alive/' + user_dead, 
       type: 'GET', 
       success: function(response) { 
            response = JSON.parse(response);
            let dead_toggle = response['dead'];
	    console.log(dead_toggle);
            if (dead_toggle){
            	deadButton.classList.remove("ready");
            	deadButton.classList.add("pause");
                deadButton.innerText = "Currently Dead";
		dead = dead_toggle;
            }
       }, 
       error: function(error) { 
           console.log(error); 
       } 
   }); 
}

function sendDeadStatus(bool){
    dead = bool;
    $.ajax({ 
       url: '/user/' + user_dead, 
       type: 'POST', 
       data: {'dead_button': bool},
       dataType: 'json',
       success: function(response) { 
       }, 
       error: function(error) { 
       } 
   }); 
   
}

function on_click(){
    if (deadButton){
	if (dead) {
	    deadButton.classList.add("ready");
	    deadButton.classList.remove("pause");
	    deadButton.innerText = "Dead";
	} else {
	    deadButton.classList.remove("ready");
	    deadButton.classList.add("pause");
	    deadButton.innerText = "Currently Dead";

	}
    }
    sendDeadStatus(!dead);
}

if(deadButton){
    getData();
    deadButton.addEventListener("click", on_click);
}
