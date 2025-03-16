document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            fetch(`/cart/add/${productId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                // Обновляем счетчик корзины
                document.querySelector('.navbar .btn-outline-primary').textContent = `Корзина (${data.total_items})`;
            });
        });
    });
});