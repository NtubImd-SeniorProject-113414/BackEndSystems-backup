const socket = new WebSocket('ws://' + window.location.host + '/ws/image/');
socket.binaryType = 'arraybuffer';

socket.onopen = function(event) {
    console.log('WebSocket 連接已建立！');
};

socket.onmessage = function(event) {
    let showModal = true;

    if (typeof event.data === 'string') {
        const parsedData = JSON.parse(event.data);

        if (parsedData.type === 'alert') {
            showAlert(parsedData.message);
        }
    } else if (event.data instanceof ArrayBuffer) {
        const blob = new Blob([event.data], { type: 'image/png' });
        const url = URL.createObjectURL(blob);

        const imageElement = document.getElementById('receivedImage');
        if (imageElement) {
            imageElement.src = url;
        }

        showAlert('收到新圖片！', true);
    }

    if (showModal) {
        $('#alarmModal').modal('show');
    }
};

socket.onerror = function(error) {
    console.error('WebSocket 發生錯誤：', error);
};

socket.onclose = function(event) {
    console.warn('WebSocket 連接已被關閉：', event);
};

function showAlert(message, isImage = false) {
    document.getElementById('alertMessage').innerText = message;

    const imageElement = document.getElementById('receivedImage');
    if (imageElement) {
        if (isImage) {
            imageElement.style.display = 'block';
        } else {
            imageElement.style.display = 'none';
        }
    }

    $('#alarmModal').modal('show');
}
