function changeRatePage(num) {
    const pages = document.querySelectorAll('.rate-page');
    pages.forEach((item, index) => {
        item.style.display = 'none';
    })

    const page = document.getElementById(`rateQuestion${num}`);
    page.style.display = 'block';
}


// ------------------------ Category slider (swiper) ---------------------------- //
let categorySlider= new Swiper(".category-slider", {
    spaceBetween: 2,
    slidesPerView: 2,
    breakpoints: {
        1624: {
            slidesPerView: 11,
            spaceBetween: 5,
        },
        1024: {
            slidesPerView: 9,
            spaceBetween: 3,
        },
        760: {
            slidesPerView: 8,
            spaceBetween: 3,
        },
        480: {
            slidesPerView: 4,
            spaceBetween: 2,
        }
    },
    navigation: {
        nextEl: '.swiper-button-next',
    }
});
// ------------------------ Category slider (swiper) ---------------------------- //
