let countdown;
const socket = new WebSocket(window.websocketUrl +'/ws/order_arrived/');

socket.onopen = function(event) {
    console.log('WebSocket 連接成功');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('從伺服器收到的消息: ', data);
    const patientImg = document.getElementById('patient_img');
    const mealImg = document.getElementById('meal_img');

    document.getElementById('patient_name').textContent = data.patient_name;
    document.getElementById('course_name').textContent = data.course_name;
    patientImg.src = data.patient_image_path;
    mealImg.src = data.course_image_path;
    
    showNotification();
};

socket.onerror = function(error) {
    console.error('WebSocket 發生錯誤: ', error);
};

socket.onclose = function(event) {
    console.log('WebSocket 連接已關閉: ', event);
};

function showNotification() {
    var notification = document.getElementById('notification');
    notification.classList.add('show');

    document.getElementById('left-eye').style.animation = 'none';
    document.getElementById('right-eye').style.animation = 'none';

    let timeLeft = 30;
    const timeLeftElement = document.getElementById('time-left');
    timeLeftElement.textContent = timeLeft;

    countdown = setInterval(function() {
        timeLeft--;
        timeLeftElement.textContent = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(countdown);
            closeNotification();
            fetch('https://node-red.medimate.tw/order_timeout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
        }
    }, 1000);
}

function closeNotification() {
    var notification = document.getElementById('notification');
    notification.classList.remove('show');

    setTimeout(function() {
        document.getElementById('left-eye').style.animation = 'blink 4.5s infinite';
        document.getElementById('right-eye').style.animation = 'blink 4.5s infinite';
    }, 500);

}

function confirmDelivery() {
    clearInterval(countdown);
    closeNotification();
    fetch('https://node-red.medimate.tw/order_ok', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    });
    alert('取餐已確認！');
}
