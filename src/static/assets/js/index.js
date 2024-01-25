let topSwiper = new Swiper(".top-slider", {
    spaceBetween: 10,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false
    },
    pagination: {
        el: ".swiper-pagination",
    },
});

let packageSwiper = new Swiper(".package-slider", {
    slidesPerView: 1,
    spaceBetween: 10,
    grabCursor: true,
    breakpoints: {
        1624: {
            slidesPerView: 5,
            spaceBetween: 20,
        },
        1024: {
            slidesPerView: 4,
            spaceBetween: 15,
        },
        760: {
            slidesPerView: 4,
            spaceBetween: 15,
        },
        480: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    }
});