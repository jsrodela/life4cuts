

let socket = new WebSocket('ws://' + window.location.host + '/ws/cam')
const cam = document.getElementById('cam');
socket.onmessage = (e) => {
    if (e.data == 'end') {
        location.href = '/framechoose';
    }
    cam.src = 'data:image/jpeg;base64,' + e.data;
//    console.log(e.data);
}


let countdown = 10;

function updateTimer() {
    countdown -= 0.1;
    if (countdown <= 0) {
        countdown = 10;
        socket.send('cap')
    }

    const num = Math.floor(countdown);

    document.getElementById("timer").innerHTML = '<div>' + num + '</div>';
}

setInterval(updateTimer, 100);