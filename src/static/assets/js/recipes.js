// ------------------------ Category swiper (top slider) ---------------------------- //
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


// ---------------------------- Add data to delete category modal -------------------------- //
$('#deleteCategory').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let title = button.data('title');

    let modal = $(this);
    modal.find('.modal-body #categoryId').val(title);
    modal.find('.modal-body #categoryTitle').text(`${title}`);
})
// ------------------------- Add data to delete category modal -------------------------- //


// ---------------------------- Add data to delete material modal -------------------------- //
$('#deleteRecipe').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let pk = button.data('pk');
    let title = button.data('title');

    let modal = $(this);
    modal.find('.modal-body #recipeId').val(pk);
    modal.find('.modal-body #recipeTitle').text(title);
})
// ------------------------- Add data to delete material modal -------------------------- //
