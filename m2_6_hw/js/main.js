document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. ДИНАМИЧЕСКИЙ КАТАЛОГ (Работает только на catalog.html) ---
    const catalogContainer = document.getElementById('catalog-container');

    if (catalogContainer) {
        // Функция отрисовки карточек
        function renderCatalog(cars) {
            catalogContainer.innerHTML = ''; 

            cars.forEach(car => {
                const cardHtml = `
                    <div class="col">
                        <div class="card h-100 border-0 shadow-sm card-car rounded-4 overflow-hidden">
                            <div class="card-img-container">
                                <img src="${car.image}" alt="${car.brand} ${car.name}" onerror="this.src='https://placehold.co/600x400?text=No+Photo'">
                            </div>
                            <div class="card-body d-flex flex-column p-4">
                                <span class="text-uppercase text-muted small fw-bold tracking-wider">${car.brand}</span>
                                <h4 class="card-title fw-bold text-dark mb-3">${car.name}</h4>
                                <p class="card-text text-secondary flex-grow-1">${car.description}</p>
                                
                                <div class="mt-3">
                                    <div class="text-muted small">Стоимость</div>
                                    <div class="fs-4 fw-bold text-dark mb-3">${car.price}</div>
                                    <button class="btn btn-outline-dark w-100 fw-bold rounded-3 btn-buy" data-id="${car.id}">
                                        Добавить в корзину
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                catalogContainer.insertAdjacentHTML('beforeend', cardHtml);
            });

            initBuyButtons();
        }

        // Загрузка данных из локального JSON файла
        fetch('data/cars.json')
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки данных каталога');
                return response.json();
            })
            .then(data => {
                renderCatalog(data);
            })
            .catch(error => {
                console.error('Ошибка:', error);
                catalogContainer.innerHTML = `<div class="alert alert-danger w-100 text-center" role="alert">Не удалось загрузить каталог товаров.</div>`;
            });

        function initBuyButtons() {
            const buyButtons = document.querySelectorAll('.btn-buy');
            buyButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const carId = e.target.getAttribute('data-id');
                    alert(`Товар (ID: ${carId}) успешно «добавлен» в корзину!`);
                });
            });
        }
    }

    // --- 2. ВАЛИДАЦИЯ ФОРМЫ (Работает только на contacts.html) ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('userName').value;
            alert(`Спасибо, ${name}! Ваша заявка успешно отправлена.`);
            contactForm.reset();
        });
    }
});
