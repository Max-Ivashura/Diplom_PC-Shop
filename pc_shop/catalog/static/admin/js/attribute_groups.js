// static/admin/js/attribute_groups.js
(function($) {
    'use strict';

    $(document).ready(function() {
        // Инициализация аккордеона
        const accordion = new bootstrap.Accordion('#attributeGroupsAccordion');

        // Обработка изменения категории
        $('#id_category').change(function() {
            const categoryId = $(this).val();
            if (categoryId) {
                $.ajax({
                    url: '{% url "admin:get_attributes" %}',
                    data: { category_id: categoryId },
                    success: function(data) {
                        $('#attribute-editor').html(data);
                        initializeSortable();
                    }
                });
            }
        });

        // Инициализация сортировки
        function initializeSortable() {
            $('.attribute-list').sortable({
                handle: '.attribute-header',
                update: function() {
                    $(this).find('.attribute-row').each(function(index) {
                        $(this).find('.attribute-order').text(index + 1);
                    });
                }
            });
        }

        // Обработка сохранения
        $('.submit-row input').click(function() {
            $('.attribute-row').each(function() {
                const attrId = $(this).data('attribute-id');
                const value = $(this).find('input').val();
                $('<input>').attr({
                    type: 'hidden',
                    name: 'attributes[' + attrId + ']',
                    value: value
                }).appendTo('form');
            });
        });
    });

})(django.jQuery);