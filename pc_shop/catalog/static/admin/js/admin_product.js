(function($) {
    function loadAttributes(category_id) {
        $.ajax({
            url: '/api/attributes/',
            data: { category_id: category_id },
            success: function(data) {
                // Очистить текущие поля атрибутов
                $('#attributevalue_set-group .tabular').html('');
                // Добавить новые поля (логика зависит от вашей структуры)
                console.log('Получены атрибуты:', data);
            }
        });
    }

    $(document).ready(function() {
        // При изменении категории
        $('#id_category').change(function() {
            const category_id = $(this).val();
            if (category_id) loadAttributes(category_id);
        });
    });
})(django.jQuery);

(function($) {
    // Drag-and-drop для изображений
    $('.image-order').sortable({
        handle: '.drag-handle',
        update: function() {
            $(this).find('input[type="hidden"]').each(function(index) {
                $(this).val(index + 1);
            });
        }
    });

    // Выбор основного изображения
    $('.image-radio').change(function() {
        $('.image-radio').not(this).prop('checked', false);
    });

    // Подсветка изменений
    $('.field-in_stock input').change(function() {
        $(this).closest('.form-row').toggleClass('in-stock-true', this.checked);
    });
})(django.jQuery);