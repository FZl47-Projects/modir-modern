// ---------------------------- Add data to delete material modal -------------------------- //
$('#deleteMaterial').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let id = button.data('id');
    let title = button.data('title');

    let modal = $(this);
    modal.find('.modal-body #materialId').val(id);
    modal.find('.modal-body #materialTitle').text(title);
})
// ------------------------- Add data to delete material modal -------------------------- //


// ---------------------------- Create new 'add recipe food form' section -------------------------- //
function createAddSection() {
    const parentDiv = document.getElementById('materialsSection');
    const firstSelect = parentDiv.firstElementChild.firstElementChild.querySelector('select');

    const newDiv = document.createElement('div');
    newDiv.className = 'd-flex align-items-end gap-1 border-bottom border-1 border-light mt-1 mb-4';
    newDiv.innerHTML = `
        <div class="d-flex flex-wrap gap-2 flex-grow-1 form-group">
            <label class="form-label fs-13 flex-grow-1 select-part">
                عنوان ماده اولیه
            </label>
            <label class="form-label fs-13 flex-grow-1">
                مقدار (کیلوگرم/عدد)
                <input type="number" name="amount" step="any" required class="form form-control f-input mt-1">
            </label>
        </div>
        <button type="button" class="btn btn-danger fw-semibold mb-2" onclick="removeSection(this)">x</button>
    `;

    const selectClone = firstSelect.cloneNode(true);
    newDiv.querySelector('.select-part').appendChild(selectClone);
    parentDiv.appendChild(newDiv);

    addSelect2();
}
// ------------------------- Create new 'add recipe food form' section -------------------------- //


// ---------------------------- Remove section by given id -------------------------- //
function removeSection(e) {
    let parent = e.parentElement;
    parent.remove();
}
// ------------------------- Remove section by given id -------------------------- //


function addSelect2(){
    $('.select-inputs').select2({
        width: '100%',
        dropdownParent: $('#addMaterials'),
    });
}
addSelect2();
