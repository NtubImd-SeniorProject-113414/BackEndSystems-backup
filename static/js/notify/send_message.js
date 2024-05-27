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
            alert("請選擇至少一個發送對象！");
        }
    });
});