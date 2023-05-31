
fetchPlayerMetadata();

function fetchPlayerMetadata() {
    username = $('#selectedPlayer').val()
    const socket = new WebSocket('ws://' + location.host + '/player/' + username);
    socket.addEventListener('message', ev => {
        data = JSON.parse(ev.data)
        document.getElementById('playerDetail').innerHTML = data.name +', ['+data.location+']'
        document.getElementById('score').innerHTML = data.score
    });
}
