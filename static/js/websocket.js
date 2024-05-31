var socket = new WebSocket('ws://' + window.location.host + '/ws/cards/');

socket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data.message;
    alert("收到通知：" + message);
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
