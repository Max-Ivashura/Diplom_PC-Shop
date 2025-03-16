document.addEventListener('DOMContentLoaded', function() {
    // Инициализация аккордеонов
    const accordionButtons = document.querySelectorAll('.accordion-button');
    accordionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.getAttribute('data-bs-target');
            const collapse = document.querySelector(target);
            if (collapse) {
                const bsCollapse = new bootstrap.Collapse(collapse);
            }
        });
    });
});