function toggleActive(warehouseId, isActive) {
    var btn = document.getElementById('toggleBtn' + warehouseId);
    // 发送 AJAX 请求来切换激活状态
    // 这里使用了 fetch API 发送 POST 请求
    fetch('/toggle_active/' + warehouseId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // 在 Django 中需要添加 CSRF token
        },
        body: JSON.stringify({}) // 可以发送一些数据，但在此示例中不需要
    })
    .then(response => response.json())
    .then(data => {
        // 更新按钮文本为切换后的状态
        if (data.success) {
            isActive = !isActive;
            btn.textContent = isActive ? '关闭' : '开启';
        } else {
            console.error('Failed to toggle active status.');
        }
    })
    .catch(error => {
        console.error('Error toggling active status:', error);
    });
}
