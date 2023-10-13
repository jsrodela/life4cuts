
let socket = new WebSocket('ws://' + window.location.host + '/ws/loading')
const percent = document.getElementById('percent')
const status = document.getElementById('status')
const tip = document.getElementById('tip')
socket.onmessage = (e) => {
    data = JSON.parse(e.data)

    percent.innerHTML = data['percent'] + '%';
    status.innerHTML = data['status']
    tip.innerHTML = data['tip']

    if (data['percent'] == 100) {
        location.href = '/end'
    }

}

function play_animation() {
    const objs = [null, percent, status, tip];
    for (let i=1;i<=3;i++) {
        let obj = objs[i];
        setTimeout(() => {
            obj.classList.remove('remove')
            obj.classList.add('anim')
        }, 500*i)
        setTimeout(() => {
            obj.classList.remove('anim')
            obj.classList.add('remove')
        }, 3500+500*i)
    }
}
setInterval(play_animation, 5000)
play_animation()

socket.send("done?")
