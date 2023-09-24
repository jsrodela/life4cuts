let socket = new WebSocket('ws://' + window.location.host + '/ws/loading')
socket.onmessage = (e) => {
    console.log(e.data)
}
