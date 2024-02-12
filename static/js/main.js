function showPopup() {
    document.getElementById('popup').style.display = 'block';
}

function hidePopup() {
    document.getElementById('popup').style.display = 'none';
}


//---------------------------------------------------------------- костыль
var selectedRowId = null;

function toggleRow(row, id) {
    if (selectedRowId === id) {
        // Если строка уже выбрана, снимаем выделение и сбрасываем состояние
        row.classList.remove('row-clicked');
        selectedRowId = null;
    } else {
        // Если строка не выбрана, снимаем выделение с предыдущей строки (если есть) и выделяем текущую
        if (selectedRowId) {
            var previousRow = document.querySelector('.row[data-id="' + selectedRowId + '"]');
            previousRow.classList.remove('row-clicked');
        }
        row.classList.add('row-clicked');
        selectedRowId = id;
    }
}

function changeData() {
    console.log(selectedRowId);
}