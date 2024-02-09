
// $.ajax({
//     url: `/restaurant/materials/${pk}/`,
//     type: 'GET',
//     success: function (data) {
//         let title = data['obj']['title'];
//         let price = data['obj']['price'];
//         let category = data['obj']['category'];
//
//         modal.find('.modal-header #headerTitle').text(`ویرایش ${title}`);
//         modal.find('.modal-body input[type=text]').val(title);
//         modal.find('.modal-body input[type=number]').val(price);
//         modal.find('.modal-body select').val(category);
//     },
//     error: function (error) {
//         console.error('Error:', error);
//     }
// });


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
    const firstSelect = parentDiv.firstElementChild.firstElementChild.querySelector('select[name=raw_material]');
    const secondSelect = parentDiv.firstElementChild.firstElementChild.querySelector('select[name=prepared_material]');

    const newDiv = document.createElement('div');
    newDiv.className = 'd-flex align-items-end gap-1 border-bottom border-1 border-light mt-1 mb-4 form-child';
    newDiv.innerHTML = `
        <div class="d-flex flex-wrap gap-2 flex-grow-1 form-group">
            <label class="form-label fs-13 flex-grow-1 material-select">
                عنوان ماده اولیه
            </label>
            <label class="form-label fs-13 flex-grow-1 prepared-select">
                ماده اولیه آماده شده
            </label>
            <label class="form-label fs-13 flex-grow-1">
                مقدار (کیلوگرم/عدد)
                <input type="number" name="amount" step="any" required class="form form-control f-input mt-1">
            </label>
        </div>
        <button type="button" class="btn btn-danger fw-semibold mb-2" onclick="removeSection(this)">x</button>
    `;

    const firstSelectClone = firstSelect.cloneNode(true);
    const secondSelectClone = secondSelect.cloneNode(true);

    newDiv.querySelector('.material-select').appendChild(firstSelectClone);
    newDiv.querySelector('.prepared-select').appendChild(secondSelectClone);

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


// ------------------------
document.getElementById('addMaterialsForm').addEventListener('submit', function (e){
    e.preventDefault();
    let submit_status = true;
    const forms = this.querySelectorAll('.form-child');

    forms.forEach((item, index) => {
        let raw_material_select = item.querySelector('select[name=raw_material]').value;
        let prepared_material_select = item.querySelector('select[name=prepared_material]').value;

        console.log(raw_material_select, prepared_material_select)

        if (submit_status) {
            if (raw_material_select === 'null' && prepared_material_select === 'null') {
                Toast.fire({
                    icon: 'info',
                    title: `لطفا یک ماده اولیه یا ماده اولیه ساخته شده انتخاب کنید`,
                });
                submit_status = false;
            } else if (raw_material_select !== 'null' && prepared_material_select !== 'null') {
                Toast.fire({
                    icon: 'info',
                    title: `صرفا یک ماده اولیه یا ماده اولیه ساخته شده انتخاب کنید`,
                });
                submit_status = false;
            }
        }
    });

    if(submit_status) {
        this.submit();
    }
})


function addSelect2(){
    $('.select-inputs').select2({
        width: '100%',
        dropdownParent: $('#addMaterials'),
    });
}
addSelect2();
