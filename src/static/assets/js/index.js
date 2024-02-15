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


// Top static banner events
const topBanner = document.querySelector('.bottom-banner');
const bannerBtnSuccess = topBanner.querySelector('.btn-success');
const bannerBtnDanger = topBanner.querySelector('.btn-danger');
let deferredPrompt = null;


function showPwaBlock() {
    if (navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|Opera Mini|IEMobile/i)) {
        topBanner.style.display = 'block';
    }
}

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    showPwaBlock();
})

bannerBtnDanger.addEventListener('click', function () {
    topBanner.style.display = 'none';
})

bannerBtnSuccess.addEventListener('click', async function () {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
            console.log('User accepted');
            topBanner.style.display = 'none';
        }
        deferredPrompt = null;
    });
})
