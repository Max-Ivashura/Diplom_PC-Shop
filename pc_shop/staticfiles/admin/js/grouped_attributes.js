document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.attributevalue_set-group .table');
    if (!table) return;

    const rows = Array.from(table.querySelectorAll('tr'));
    const groups = {};

    rows.forEach(row => {
        const groupCell = row.querySelector('.field-attribute .select option:checked');
        if (!groupCell) return;

        const groupName = groupCell.text.split(' - ')[0];
        if (!groups[groupName]) {
            groups[groupName] = [];
        }
        groups[groupName].push(row);
    });

    Object.keys(groups).sort().forEach(groupName => {
        const groupRows = groups[groupName].sort((a, b) => {
            const aOrder = a.querySelector('.field-attribute').textContent.match(/order=(\d+)/)[1];
            const bOrder = b.querySelector('.field-attribute').textContent.match(/order=(\d+)/)[1];
            return aOrder - bOrder;
        });
        groupRows.forEach(row => table.appendChild(row));
    });
});