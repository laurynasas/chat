var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function () {
    $messages.mCustomScrollbar();
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage(msg, is_it_me) {
    if ($.trim(msg) == '') {
        return false;
    }
    if (is_it_me === true) {
        $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    } else if (is_it_me === false) {
        $('<div class="message new">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    }
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
}