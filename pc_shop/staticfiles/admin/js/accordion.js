document.addEventListener('DOMContentLoaded', function() {
  // Инициализация аккордеона Bootstrap
  var accordion = document.getElementById('attributeAccordion');
  if (accordion) {
    var bsAccordion = new bootstrap.Accordion(accordion);
  }
});