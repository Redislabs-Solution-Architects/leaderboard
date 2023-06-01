
fetchPlayerMetadata();

function fetchPlayerMetadata() {
    username = $('#selectedPlayer').val()
    const socket = new WebSocket('ws://' + location.host + '/player/' + username);
    socket.addEventListener('message', ev => {
        data = JSON.parse(ev.data)
        document.getElementById('playerDetail').innerHTML = data.name +'&nbsp;<span class="badge rounded-pill bg-warning text-dark">'+data.location+'</span>'
        document.getElementById('score').innerHTML = '<span class="badge rounded-pill bg-warning text-dark">'+data.score+'</span>'
    });
}
