(function($) {
    'use strict';

    $(document).ready(function() {
        // Проверка работоспособности
        $('#attribute-editor').addClass('debug-border');

        // Удаление атрибута
        $('.delete-attr').on('click', function() {
            const row = $(this).closest('.attribute-row');
            row.hide('slow', function() {
                row.remove();
            });
        });

        // Подсветка обязательных полей
        $('[data-required="true"]').closest('.attribute-row').find('input, select').addClass('is-invalid');
    });

})(django.jQuery);