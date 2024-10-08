
fetchActivePlayers();
fetchLeaderboardData();
fetchActiveRegionalPlayers();

function fetchActivePlayers() {
    const socket = new WebSocket('ws://' + location.host + '/players');
    text = '<li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="/overview?username=plyr">'
        +'<span class="d-inline-block bg-success rounded-circle" style="width: .5em; height: .5em;"></span>plyr'
        +'<span class="badge bg-dark"> Location: loctn</span></a></li>'
    socket.addEventListener('message', ev => {
        data = JSON.parse(ev.data)
        if (data.hasOwnProperty('_NODATA')) {
            $('#playerContainer').html('')
        } else {
            replacedText = text.replaceAll('plyr', data.username)
            replacedText = replacedText.replace('loctn', data.location)
            $('#playerContainer').append(replacedText)
        }
    });
}

function fetchActiveRegionalPlayers() {
    const socket3 = new WebSocket('ws://' + location.host + '/regional-players');
    text3 = '<li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="/overview?username=plyer">'
        +'<span class="d-inline-block bg-success rounded-circle" style="width: .5em; height: .5em;"></span>plyer</a></li>'
    socket3.addEventListener('message', ev => {
        data = JSON.parse(ev.data)
        if (data.hasOwnProperty('_NODATA')) {
            $('#regPlayerContainer').html('')
        } else {
            replacedText = text3.replaceAll('plyer', data.username)
            $('#regPlayerContainer').append(replacedText)
        }
    });
}

function fetchLeaderboardData() {
    const socket2 = new WebSocket('ws://' + location.host + '/game/leaderboard');
    $('#leaderboardContainer').html('')
    text2 = '<li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#"><span class="d-inline-block bg-success rounded-circle" style="width: .5em; height: .5em;"></span>player<span class="badge rounded-pill bg-info text-dark"> score</span></a></li>'
    socket2.addEventListener('message', ev => {
        data = JSON.parse(ev.data)
        if (data.hasOwnProperty('_NODATA')) {
            $('#leaderboardContainer').html('')
        } else {
            replacedText = text2.replace('player', data.player.replace('player:',''))
            replacedText = replacedText.replace('score', data.score)
            $('#leaderboardContainer').append(replacedText)
        }
    });
}
