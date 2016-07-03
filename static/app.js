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
        if (keyName)
            keyStates[keyName] = true;
    });
    $(document).on('keyup', function (event) {
        var keyName = keyNames[event.which];
        if (keyName) {
            keyStates[keyName] = false;
            $.ajax('/key/' + keyName + '/release');
        }
    });
});
