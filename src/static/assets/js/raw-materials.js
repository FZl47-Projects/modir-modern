// ------------------------ Category slider (swiper) ---------------------------- //
let categorySlider = new Swiper(".category-slider", {
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
});
// ------------------------ Category slider (swiper) ---------------------------- //

// ---------------------------- Add data to request modal -------------------------- //
$('#confirmPurchaseModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let primaryKey = button.data('primarykey');
    let title = button.data('title')

    let modal = $(this);
    modal.find('.modal-body #subscriptionId').val(primaryKey);
    modal.find('.modal-body #subscriptionTitle').text(`${title}`);
})
// ------------------------- Add data to request  modal -------------------------- //
