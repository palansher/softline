document.addEventListener('DOMContentLoaded', () => {
    const display = document.getElementById('display');
    const buttons = document.querySelectorAll('.btn');
    let isResultState = false;

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const val = button.getAttribute('data-val');
            const action = button.getAttribute('data-action');

            if (action === 'clear') {
                clearDisplay();
            } else if (action === 'backspace') {
                handleBackspace();
            } else if (button.id === 'equals-btn') {
                calculateResult();
            } else if (val !== null) {
                appendCharacter(val);
            }
        });
    });

    function appendCharacter(char) {
        
        display.classList.remove('error-state');

        if (display.value === '0' || isResultState) {
            // Если предыдущая операция вернула результат — начинаем ввод заново,
            // либо дописываем знак операции к текущему результату
            if (isResultState && ['+', '-', '*', '/'].includes(char)) {
                isResultState = false;
            } else {
                display.value = '';
                isResultState = false;
            }
        }
        display.value += char;
    }

    function clearDisplay() {
        display.classList.remove('error-state');
        display.value = '0';
        isResultState = false;
    }

    function handleBackspace() {
        if (isResultState) {
            clearDisplay();
            return;
        }
        display.value = display.value.slice(0, -1);
        if (display.value === '') {
            display.value = '0';
        }
    }

    async function calculateResult() {
        const expression = display.value;
        if (!expression) return;

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ expression: expression })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                display.value = data.result;
                display.classList.remove('error-state'); // Сбрасываем ошибку
                isResultState = true;
            } else {
                display.value = data.message || 'Ошибка';
                display.classList.add('error-state');    // Включаем стиль ошибки
                isResultState = true;
            }
        } catch (error) {
            display.value = 'Ошибка сети';
            isResultState = true;
        }
    }
});
