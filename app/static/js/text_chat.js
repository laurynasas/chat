var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    socket.emit('my event', {
        data: 'User Connected'
    });


    // $(window).on('keydown', function (e) {
    //     socket.emit('my event', {
    //         user_name: "You",
    //         message: msg
    //     });
    //     if (e.which == 13) {
    //         insertMessage();
    //         return false;
    //     }
    // })
    $('.message-submit').click(function () {
        msg = $('.message-input').val();
        current_user_id = $('#current-user').data("current-user");
        socket.emit('my event', {
            sender:current_user_id,
            message: msg
        });
        // insertMessage(msg);
    })
});
socket.on('my response', function (payload) {
    receiver = $('#current-user').data("current-user");
    if (typeof receiver !== 'undefined') {
        if (receiver === payload.sender) {
            insertMessage(payload.message, true);
        } else {
            insertMessage(payload.message, false);
        }

    }
})