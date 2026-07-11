document.addEventListener('DOMContentLoaded', () => {

    // --- 1. ДИНАМИЧЕСКИЙ КАТАЛОГ (Работает только на catalog.html) ---
    const catalogContainer = document.getElementById('catalog-container');


    if (catalogContainer) {

        const buyButtons = document.querySelectorAll('.btn-buy');
        buyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const carId = e.target.getAttribute('data-id');
                alert(`Товар (ID: ${carId}) успешно «добавлен» в корзину!`);
            });
        });

    }

});
