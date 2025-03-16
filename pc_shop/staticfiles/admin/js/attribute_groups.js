document.addEventListener('DOMContentLoaded', function() {
    const groups = {};

    // Группируем атрибуты по группам
    document.querySelectorAll('.attributevalue_set tr').forEach(row => {
        const groupName = row.querySelector('.field-attribute select option:selected').text.split(' - ')[0];
        if (!groups[groupName]) groups[groupName] = [];
        groups[groupName].push(row);
    });

    // Создаем аккордеон
    for (const [groupName, rows] of Object.entries(groups)) {
        const header = document.createElement('h3');
        header.textContent = groupName;
        header.style.cursor = 'pointer';
        header.classList.add('group-header');

        const container = document.createElement('div');
        container.classList.add('group-container');
        rows.forEach(row => container.appendChild(row));

        document.querySelector('.attributevalue_set').prepend(container);
        document.querySelector('.attributevalue_set').prepend(header);
    }

    // Обработчик кликов
    document.querySelectorAll('.group-header').forEach(header => {
        header.addEventListener('click', () => {
            const container = header.nextElementSibling;
            container.style.display = container.style.display === 'none' ? 'block' : 'none';
        });
    });
});