document.addEventListener('DOMContentLoaded', () => {
    // Гамбургер-меню
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');
    
    navToggle.addEventListener('click', () => {
        nav.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Подсветка активного пункта меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Клиентская валидация формы в модальном окне
    const form = document.getElementById('addPartnerForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            const inn = document.getElementById('inn').value;
            const phone = document.getElementById('phone').value;
            const email = document.getElementById('email').value;

            if (inn && !/^\d{10,12}$/.test(inn)) {
                e.preventDefault();
                alert('ИНН должен содержать 10 или 12 цифр');
            }
            if (phone && !/^\+?\d{10,15}$/.test(phone)) {
                e.preventDefault();
                alert('Телефон должен содержать 10–15 цифр');
            }
            if (email && !/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email)) {
                e.preventDefault();
                alert('Неверный формат Email');
            }
        });
    }
});