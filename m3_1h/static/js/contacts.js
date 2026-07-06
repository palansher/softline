document.addEventListener('DOMContentLoaded', () => {


    // ВАЛИДАЦИЯ ФОРМЫ (Работает только на contacts.html) ---
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
