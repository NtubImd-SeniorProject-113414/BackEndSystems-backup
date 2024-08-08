$(document).ready(function() {
    const choicesInstances = [];
    $('.choices').each(function() {
        const instance = new Choices(this, {
            removeItemButton: true,
            searchEnabled: true,
        });
        choicesInstances.push(instance);
    });

    $('#select-all-btn').click(function() {
        choicesInstances.forEach(function(instance) {
            const allValues = [];
            instance._currentState.choices.forEach(function(choice) {
                if (!choice.selected) {
                    allValues.push(choice.value);
                }
            });
            instance.setChoiceByValue(allValues);
        });
    });

    $('#clear-all-btn').click(function() {
        choicesInstances.forEach(function(instance) {
            instance.removeActiveItems();
        });
    });

    $('#notification-form').submit(function(event) {
        const messageValue = $('#id_notify_message').val().trim();
        let hasSelection = false;
        choicesInstances.forEach(function(instance) {
            if (instance.getValue(true).length > 0) {
                hasSelection = true;
            }
        });
        if (!messageValue) {
            event.preventDefault();
            alert("請輸入要發送的訊息！");
            return;
        }
        if (!hasSelection) {
            event.preventDefault();
            alert("請選擇至少一個對象！");
        }
    });

    $('#print-qrcode-form').submit(function(event) {
        event.preventDefault();
        
        let hasSelection = false;
        choicesInstances.forEach(function(instance) {
            if (instance.getValue(true).length > 0) {
                hasSelection = true;
            }
        });
    
        if (!hasSelection) {
            alert("請選擇至少一個對象！");
            return;
        }
    
        let formData = new FormData(this);
        $('#preloaderModal').modal('show');
    
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhrFields: {
                responseType: 'blob'
            },
            success: function(data, status, xhr) {
                $('#preloaderModal').modal('hide');
                let disposition = xhr.getResponseHeader('Content-Disposition');
                let filename = "stop_point_report.pdf";
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    let matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) { 
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }
    
                let blob = new Blob([data], { type: 'application/pdf' });
                let link = document.createElement('a');
                let url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
    
                window.URL.revokeObjectURL(url);
            },
            error: function() {
                alert("發生錯誤！");
            }
        });
    });
});