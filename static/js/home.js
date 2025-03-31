// carousal
    document.addEventListener('DOMContentLoaded', function () {
        var swiper = new Swiper(".swiper", {
            loop: true,
            autoplay: {
                delay: 2000,
                disableOnInteraction: false,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
    });

// mobile menu
const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navber');

if (bar) {
    bar.addEventListener('click', () => {
        nav.classList.add('active');
    })
}

if (close) {
    close.addEventListener('click', () => {
        nav.classList.remove('active');
    })
}


