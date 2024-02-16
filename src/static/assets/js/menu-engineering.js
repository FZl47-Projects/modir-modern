// ------------------------ Category slider (swiper) ---------------------------- //
let categorySwiper= new Swiper(".category-slider", {
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


// ------------------------- Print menu engineering page ------------------------------- //
function printThis() {
    let menu = document.getElementById('SideMenu');
    let printObjs = document.querySelectorAll('.print-obj');
    let container = document.querySelector('.container-fluid');

    printObjs.forEach((item, index) => {
       item.classList.add('d-none');
    });

    menu.style.display = 'none';
    container.classList.replace('col-md-10', 'col-12');

    window.print();

    menu.style.display = 'block';
    container.classList.replace('col-12', 'col-md-10');

    printObjs.forEach((item, index) => {
       item.classList.remove('d-none');
    });
}
// ------------------------- Print menu engineering page ------------------------------- //


// --------------------------- Submit form with ajax and get results -------------------- //
function submitFormAjax(e) {
    e.preventDefault();
    $.ajax({
        url: $(e).attr('action'),
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,

        success: function(response) {
            $("#form").trigger("reset"); // to reset form input fields
        },
        error: function(e) {
            console.log(e);
        }
    });
}
// --------------------------- Submit form with ajax and get results -------------------- //
