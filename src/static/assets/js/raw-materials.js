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
$('#deleteMaterial').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let title = button.data('title');
    let pk = button.data('pk');

    let modal = $(this);
    modal.find('.modal-body #materialPK').val(pk);
    modal.find('.modal-body #materialTitle').text(title);
})
// ------------------------- Add data to delete material modal -------------------------- //


// ---------------------------- Add data to edit material modal -------------------------- //
$('#editMaterial').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let modal = $(this);

    let pk = button.data('pk');
    let title = button.data('title');
    let use_for = button.data('use');
    let price = button.data('price');
    let category = button.data('category');

    modal.find('.modal-dialog #editMaterialForm').attr('action', `/restaurant/materials/${pk}/edit/`)
    modal.find('.modal-body input[name=title]').val(title);
    modal.find('.modal-body input[name=use_for]').val(use_for);
    modal.find('.modal-body input[type=number]').val(price);
    modal.find('.modal-body select').val(category);
})
// ------------------------- Add data to edit material modal -------------------------- //


// ---------------------------- Create new add material form section -------------------------- //
function createNewSection() {
    const parentDiv = document.getElementById('materialsSection');
    const firstSelect = parentDiv.firstElementChild.querySelector('select');

    const newDiv = document.createElement('div');
    newDiv.className = 'd-flex align-items-end gap-1 border-bottom border-1 border-light mt-5 form-group';
    newDiv.innerHTML = `
        <div class="d-flex align-items-end flex-wrap gap-2 w-100">
            <label class="form-label fs-13 flex-grow-1">
                عنوان ماده اولیه
                <input type="text" name="title" class="form form-control f-input mt-1" required>
            </label>
            <label class="form-label fs-13 flex-grow-1">
                مورد استفاده
                <input type="text" name="use_for" class="form form-control f-input mt-1">
            </label>
            <label class="form-label fs-13 flex-grow-1">
                <span>
                    قیمت به ازای هر واحد
                    <small>(تومان)</small>
                </span>
                <input type="number" name="price" minlength="0" class="form form-control f-input mt-1" required>
            </label>
            <label class="form-label fs-13 flex-grow-1 select-part">
                دسته بندی
                
            </label>
            <button type="button" class="btn btn-danger fw-semibold mb-2" onclick="removeSection(this)">x</button>
        </div>
    `;

    const selectClone = firstSelect.cloneNode(true);
    newDiv.querySelector('.select-part').appendChild(selectClone);

    parentDiv.appendChild(newDiv);
}
// ------------------------- Create new add material form section -------------------------- //


// ---------------------------- Remove section by given id -------------------------- //
function removeSection(e) {
    let parent = e.parentElement.parentElement;
    parent.remove();
}
// ------------------------- Remove section by given id -------------------------- //
