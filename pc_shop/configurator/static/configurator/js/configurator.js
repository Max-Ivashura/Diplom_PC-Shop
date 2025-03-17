document.querySelectorAll('.component-card.selectable').forEach(card => {
    card.addEventListener('click', function() {
        const categoryId = this.dataset.category;
        const url = `/catalog/?category=${encodeURIComponent(categoryId)}`;
        window.location.href = url;
    });
});

// Обновление миниатюры после выбора компонента
function updateComponentCard(categoryId, productData) {
    const card = document.querySelector(`.component-card[data-category="${categoryId}"]`);
    if (card) {
        card.querySelector('.component-image img').src = productData.image;
        card.classList.remove('selectable');
        card.querySelector('.placeholder').classList.remove('placeholder');
    }
}

// Проверка совместимости при изменении компонентов
function checkCompatibility() {
    const componentIds = Array.from(document.querySelectorAll('.component-card:not(.selectable)'))
        .map(card => card.dataset.productId);

    fetch('/configurator/check-compatibility/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ components: componentIds })
    })
    .then(response => response.json())
    .then(data => {
        const errorsDiv = document.getElementById('compatibilityErrors');
        errorsDiv.innerHTML = data.errors.map(error => `<div>${error}</div>`).join('');
        errorsDiv.style.display = data.errors.length ? 'block' : 'none';

        // Обновление статусов совместимости
        data.compatibility_status.forEach(status => {
            const card = document.querySelector(`.component-card[data-category="${status.category_id}"]`);
            const statusDiv = card.querySelector('.compatibility-status');
            statusDiv.textContent = status.message;
            statusDiv.className = `compatibility-status ${status.is_compatible ? 'compatibility-ok' : 'compatibility-error'}`;
        });
    });
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    checkCompatibility();
});