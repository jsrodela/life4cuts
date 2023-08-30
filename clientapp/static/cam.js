
let countdown = 10; 

function updateTimer() {
    countdown -= 0.1; 
    if (countdown <= 0) {
        countdown = 10; 
    }

    const num = Math.floor(countdown); 

    document.getElementById("timer").innerHTML = '<div>' + num + '</div>';
}

setInterval(updateTimer, 100);