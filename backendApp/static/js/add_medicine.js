document.getElementById('medicine_selection').addEventListener('change', function() {
    var selectedValue = this.value;
    if (selectedValue === 'new') {
        document.getElementById('new_medicine_fields').style.display = 'block';
        document.getElementById('stock_level_field').style.display = 'none'; // 隐藏库存和购买数量字段
    } else if (selectedValue !== '') { // 如果选择了已有的药品
        var stockLevel = document.querySelector('option[value="' + selectedValue + '"]').getAttribute('data-stock');
        document.getElementById('stock_level').textContent = stockLevel; // 设置库存
        document.getElementById('stock_level_field').style.display = 'block'; // 显示库存和购买数量字段
        document.getElementById('new_medicine_fields').style.display = 'none'; // 隐藏新增药品字段
    } else {
        document.getElementById('new_medicine_fields').style.display = 'none';
        document.getElementById('stock_level_field').style.display = 'none'; // 隐藏库存和购买数量字段
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var medicineSelection = document.getElementById('medicine_selection');
    var newMedicineFields = document.getElementById('new_medicine_fields');
    var stockLevelField = document.getElementById('stock_level_field');

    medicineSelection.addEventListener('change', function() {
        var selectedValue = this.value;
        if (selectedValue === 'new') {
            newMedicineFields.style.display = 'block';
            stockLevelField.style.display = 'none'; // 隐藏库存和购买数量字段
        } else if (selectedValue !== '') { // 如果选择了已有的药品
            var stockLevel = document.querySelector('option[value="' + selectedValue + '"]').getAttribute('data-stock');
            document.getElementById('stock_level').textContent = stockLevel; // 设置库存
            stockLevelField.style.display = 'block'; // 显示库存和购买数量字段
            newMedicineFields.style.display = 'none'; // 隐藏新增药品字段
        } else {
            newMedicineFields.style.display = 'none';
            stockLevelField.style.display = 'none'; // 隐藏库存和购买数量字段
        }
    });
});
