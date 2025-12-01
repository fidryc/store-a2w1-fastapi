// Смена главного изображения товара
function changeImage(imageSrc, thumbnailElement) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = imageSrc;
        
        // Обновляем активный thumbnail
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        if (thumbnailElement) {
            thumbnailElement.classList.add('active');
        }
        
        // Обновляем индикаторы
        const thumbnails = Array.from(document.querySelectorAll('.thumbnail'));
        const index = thumbnails.indexOf(thumbnailElement);
        document.querySelectorAll('.indicator').forEach((indicator, i) => {
            indicator.classList.toggle('active', i === index);
        });
    }
}

// Выбор размера
document.addEventListener('DOMContentLoaded', () => {
    // Обработчик для кнопок размера
    const sizeButtons = document.querySelectorAll('.size-btn');
    sizeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            sizeButtons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Обработчик для кнопок цвета
    const colorButtons = document.querySelectorAll('.color-btn');
    colorButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            colorButtons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Карусель изображений (свайп для мобильных)
    const mainImage = document.querySelector('.main-image');
    if (mainImage) {
        let startX = 0;
        let currentIndex = 0;
        const thumbnails = document.querySelectorAll('.thumbnail');
        
        mainImage.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        mainImage.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const diff = startX - endX;
            
            if (Math.abs(diff) > 50) {
                if (diff > 0 && currentIndex < thumbnails.length - 1) {
                    // Свайп влево
                    currentIndex++;
                } else if (diff < 0 && currentIndex > 0) {
                    // Свайп вправо
                    currentIndex--;
                }
                
                if (thumbnails[currentIndex]) {
                    thumbnails[currentIndex].click();
                }
            }
        });
    }
    
    // Обработчик кнопки "Заказать"
    const orderBtn = document.querySelector('.btn-order');
    if (orderBtn && !orderBtn.disabled) {
        orderBtn.addEventListener('click', () => {
            // Открываем Telegram
            window.open('https://t.me/a2w1', '_blank');
        });
    }
    
    // Плавная прокрутка к якорям
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Индикаторы карусели
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            const thumbnails = document.querySelectorAll('.thumbnail');
            if (thumbnails[index]) {
                thumbnails[index].click();
            }
        });
    });
});

// Ленивая загрузка изображений
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}