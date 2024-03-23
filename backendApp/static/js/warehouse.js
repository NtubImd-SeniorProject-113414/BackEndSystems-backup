document.querySelectorAll('.toggle-status-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var warehouseId = this.dataset.warehouseId; // 从按钮的数据集中获取仓库ID
        console.log('Warehouse ID:', warehouseId); // 添加调试语句
        if (warehouseId) {
            fetch(`/toggle-warehouse-status/${warehouseId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // 获取CSRF令牌的函数
                },
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload(); // 刷新页面以更新状态
                } else {
                    console.error('Failed to toggle warehouse status');
                }
            })
            .catch(error => {
                console.error('Error toggling warehouse status:', error);
            });
        } else {
            console.error('Warehouse ID is missing');
        }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
