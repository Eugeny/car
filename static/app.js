var keyNames = {};
keyNames[37] = 'left';
keyNames[38] = 'up';
keyNames[39] = 'right';
keyNames[40] = 'down';

var keyStates = {};

setInterval(function () {
    for (var i = 0; i < 4; i++) {
        var keyName = ['up', 'down', 'left', 'right'][i];
        if (keyStates[keyName])
            $.ajax('/key/' + keyName + '/press');
    }
}, 200);

$(function () {
    $(document).on('keydown', function (event) {
        var keyName = keyNames[event.which];
        if (keyName) {
            keyStates[keyName] = true;
            $('#button-' + keyName).addClass('btn-active');
        }
    });
    $(document).on('keyup', function (event) {
        var keyName = keyNames[event.which];
        if (keyName) {
            keyStates[keyName] = false;
            $.ajax('/key/' + keyName + '/release');
            $('#button-' + keyName).removeClass('btn-active');
        }
    });
});


$(function () {
    flowplayer("player", "/static/flow/flowplayer-3.2.3.swf", {
        debug: true,
        log: { level: 'info', filter: '*' },
        clip: {
            url: 'test',
            provider: 'rtmp',
            live: true,
            autoPlay: true,
            bufferLength: 0.1,
        },
        plugins: {
            rtmp: {
                url: '/static/flow/flowplayer.rtmp-3.2.3.swf',
                netConnectionUrl: 'rtmp://ajenti.org/flvplayback',
            },
            controls: {
                url: '/static/flow/flowplayer.controls-3.2.3.swf',
            }
        }
    });
});
