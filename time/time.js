const weekElement = document.querySelector('.week')
const hourElement = document.querySelector('.hours');
const minElement = document.querySelector('.min');
const secElement = document.querySelector('.sec');
const dayElement = document.querySelector('.day');
const dotElements = document.querySelectorAll('.dot');
let showDot = true;

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const dayIndex = now.getDay();


    hourElement.textContent = hours;
    minElement.textContent = minutes;
    secElement.textContent = seconds;
    dayElement.textContent = ['YAK', 'DUSH', 'SESH', 'CHOR', 'PAY', 'JUMA', 'SHAN', 'YAK'][dayIndex];

    // Nuqtani ko'rsatish va yashirish
    showDot = !showDot;
    dotElements.forEach(dot => dot.style.visibility = showDot ? 'visible' : 'hidden');
}

// Har 1000 millisekundda yangilanish
setInterval(updateClock, 500);
updateClock(); // Sahifa yuklanganda birinchi marta yangilash