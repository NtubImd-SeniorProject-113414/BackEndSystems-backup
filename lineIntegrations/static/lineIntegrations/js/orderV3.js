function submitOrder(courseName, courseId) {
    var confirmation = confirm("您目前選擇了「" + courseName + "」，確定要提交訂單了嗎？");
    if (confirmation) {
        $.ajax({
            type: "POST",
            url: window.location.href,
            data: { courseId: courseId },
            success: function(data) {
                window.location.reload()
            },
            error: function() {
                alert("提交訂單失敗");
            }
        });
    }
}