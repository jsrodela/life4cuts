

let socket = new WebSocket('ws://' + window.location.host + '/ws/cam')
const cam = document.getElementById('cam');
socket.onmessage = (e) => {
    if (e.data == 'end') {
        location.href = '/framechoose';
        remove();
    }
    else if (e.data == 'resume') {
        if (cnt >= MAX_CNT) {
            socket.send(JSON.stringify({
                'type': 'end'
            }))
        }
        else {
            capturing = false;
            countdown = 10;
            change_time();
            cnt++;
            change_count();
        }
    }

    cam.src = 'data:image/jpeg;base64,' + e.data; // black on resume
    // console.log(e.data);
}


let countdown = 10;
let cnt = 1;
const MAX_CNT = 6;
let capturing = false;

const shutter = document.getElementById('shutter');

function updateTimer() {
    if (!capturing)
    {
        countdown -= 0.1;
        change_time()
        if (countdown < 1) {
            // countdown = 10;
            capturing = true;
            socket.send(JSON.stringify({
                'type': 'cap',
                'num': cnt
            }))
            shutter.currentTime = 0;
            shutter.play();
        }
    }
    else
    {
        // nothing?
    }

}

function change_time() {
    const num = Math.floor(countdown);
    document.getElementById("timer").innerHTML = '<div>' + num + '</div>';
}
function change_count() {
    document.getElementById("count").innerHTML = cnt + '/' + MAX_CNT;
}

document.getElementById('start').onclick = function(obj) {
    document.querySelector('.cover').style = "opacity: 0;";
    document.querySelector('.popup').classList.add('remove')
    setInterval(updateTimer, 100);
    obj.disabled = true;
    setTimeout(() => document.querySelector('.popup').remove());
    change_count()
    change_time()
}