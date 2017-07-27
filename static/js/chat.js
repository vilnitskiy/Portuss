$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var element = $('<tr></tr>')

        element.append(
            $("<td></td>").text(data.timestamp)
        )
        element.append(
            $("<td></td>").text(data.author)
        )
        element.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(element)
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});