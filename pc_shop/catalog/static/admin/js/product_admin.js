// Автоматический выбор главного изображения
document.querySelectorAll('.field-is_main input').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            document.querySelectorAll('.field-is_main input')
                .forEach(c => c !== this && (c.checked = false));
        }
    });
});