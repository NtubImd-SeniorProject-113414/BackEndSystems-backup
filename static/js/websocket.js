const socket = new WebSocket('ws://' + window.location.host + '/ws/image/');
socket.binaryType = 'arraybuffer';

socket.onopen = function(event) {
    console.log('WebSocket 連接已建立！');
};

socket.onmessage = function(event) {
    let showModal = true;

    if (typeof event.data === 'string') {
        const parsedData = JSON.parse(event.data);

        if (parsedData.type === 'alarm') {
            showalarm(parsedData.message);
        }
    } else if (event.data instanceof ArrayBuffer) {
        const blob = new Blob([event.data], { type: 'image/png' });
        const url = URL.createObjectURL(blob);

        const imageElement = document.getElementById('receivedImage');
        if (imageElement) {
            imageElement.src = url;
        }

        showalarm('收到新圖片！', true);
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



function showalarm(message, isImage = false) {
    document.getElementById('alarmMessage').innerText = message;

    $('#alarmModal').on('show.bs.modal', function () {
        $(this).css('z-index', 8888);
        setTimeout(function () {
            $('.modal-backdrop').last().attr('data-modal-id', 'alarmModal');
            $('.modal-backdrop[data-modal-id="alarmModal"]').css('z-index', 8887);
        }, 0);
    });
    $('#alarmModal').on('hidden.bs.modal', function() {
        if (alarmSound) {
            alarmSound.pause();
            alarmSound.currentTime = 0;
        }
    });

    const imageElement = document.getElementById('receivedImage');
    if (imageElement) {
        if (isImage) {
            imageElement.style.display = 'block';
        } else {
            imageElement.style.display = 'none';
        }
    }

    const alarmSound = document.getElementById('alarmSound');
    if (alarmSound) {
        alarmSound.play();
    }

    $('#alarmModal').modal('show');
}
