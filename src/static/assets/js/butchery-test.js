
const quantity_raw_press= document.getElementById('quantity_raw_press');
const quantity_baked_press= document.getElementById('quantity_baked_press');
const price= document.getElementById('price');

const raw_usable_quantity_cost = document.getElementById('raw_usable_quantity_cost');
const raw_usable_quantity_cost_match = document.getElementById('raw_usable_quantity_cost_match');

const delivery_weight = document.getElementById('delivery_weight');
const delivery_weight_match = document.getElementById('delivery_weight_match');

const weight_loss_cleaning_unusable = document.getElementById('weight_loss_cleaning_unusable');
const weight_loss_cleaning_unusable_percent = document.getElementById('weight_loss_cleaning_unusable_percent');

const weight_loss_cleaning_usable = document.getElementById('weight_loss_cleaning_usable');
const weight_loss_cleaning_usable_percent = document.getElementById('weight_loss_cleaning_usable_percent');

const edible_cleaned_weight = document.getElementById('edible_cleaned_weight');
const edible_cleaned_weight_percent = document.getElementById('edible_cleaned_weight_percent');

const edible_cleaned_weight_match = document.getElementById('edible_cleaned_weight_match');
const edible_cleaned_weight_match_percent = document.getElementById('edible_cleaned_weight_match_percent');

const weight_loss_baking = document.getElementById('weight_loss_baking');
const weight_loss_baking_percent = document.getElementById('weight_loss_baking_percent');

const salable_weight = document.getElementById('salable_weight');
const salable_weight_percent = document.getElementById('salable_weight_percent');

const edible_cleaned_weight_percent_match = document.getElementById('edible_cleaned_weight_percent_match');
const salable_weight_percent_match = document.getElementById('salable_weight_percent_match');
const baked_usable_quantity_cost = document.getElementById('baked_usable_quantity_cost');
const raw_usable_quantity_cost_per_press = document.getElementById('raw_usable_quantity_cost_per_press');
const baked_usable_quantity_cost_per_press = document.getElementById('baked_usable_quantity_cost_per_press');
const number_of_raw_use = document.getElementById('number_of_raw_use');
const number_of_baked_use = document.getElementById('number_of_baked_use');


// Change related inputs functions //
function change_weight_loss_cleaning_unusable_percent() {
    let percent = ((weight_loss_cleaning_unusable.value / delivery_weight.value) * 100).toFixed(2);
    weight_loss_cleaning_unusable_percent.value = Number(percent) || 0;
}

function change_weight_loss_cleaning_usable_percent() {
    let percent = ((weight_loss_cleaning_usable.value / delivery_weight.value) * 100).toFixed(2);
    weight_loss_cleaning_usable_percent.value = Number(percent) || 0;
}

function change_edible_cleaned_weight() {
    let input1 = Number(delivery_weight_match.value * 100);
    let input2 = Number(weight_loss_cleaning_unusable.value * 100);
    let input3 = Number(weight_loss_cleaning_usable.value * 100);

    edible_cleaned_weight.value = (input1 - (input2 + input3)) / 100;

    let percent = ((edible_cleaned_weight.value / delivery_weight_match.value) * 100).toFixed(2);
    edible_cleaned_weight_percent.value = Number(percent) || 0;

    change_edible_cleaned_weight_match();
}

function change_edible_cleaned_weight_match() {
    edible_cleaned_weight_match.value = edible_cleaned_weight.value;
    edible_cleaned_weight_match_percent.value = edible_cleaned_weight_percent.value;

    change_weight_loss_baking_percent();
}

function change_weight_loss_baking_percent() {
    let percent = ((weight_loss_baking.value / edible_cleaned_weight_match.value) * 100).toFixed(2);
    weight_loss_baking_percent.value = Number(percent) || 0;

    change_salable_weight();
}

function change_salable_weight() {
    let input1 = Number(edible_cleaned_weight_match.value * 100);
    let input2 = Number(weight_loss_baking.value * 100);
    salable_weight.value = (input1 - input2) / 100;

    let percent = ((salable_weight.value / edible_cleaned_weight_match.value) * 100).toFixed(2);
    salable_weight_percent.value = Number(percent) || 0;

    change_edible_cleaned_weight_percent_match();
    change_salable_weight_percent_match();
}

function change_edible_cleaned_weight_percent_match() {
    edible_cleaned_weight_percent_match.value = edible_cleaned_weight_percent.value;
}

function change_salable_weight_percent_match() {
    salable_weight_percent_match.value = salable_weight_percent.value;
}
// .End Change related inputs functions //


// AddEventListeners functions
delivery_weight.addEventListener('input', function (e){
    delivery_weight_match.value = Number(e.target.value);

    change_weight_loss_cleaning_unusable_percent();
    change_weight_loss_cleaning_usable_percent();
    change_edible_cleaned_weight();
});

weight_loss_cleaning_unusable.addEventListener('input', function (e){
    let percent = ((e.target.value / delivery_weight_match.value) * 100).toFixed(2);
    weight_loss_cleaning_unusable_percent.value = Number(percent);

    change_edible_cleaned_weight();
});

weight_loss_cleaning_usable.addEventListener('input', function (e){
    let percent = ((e.target.value / delivery_weight_match.value) * 100).toFixed(2);
    weight_loss_cleaning_usable_percent.value = Number(percent);

    change_edible_cleaned_weight();
});

weight_loss_baking.addEventListener('input', function (e) {
    change_weight_loss_baking_percent();
});
// .End AddEventListeners functions //


window.addEventListener('load', function (){
    change_weight_loss_cleaning_unusable_percent();
    change_weight_loss_cleaning_usable_percent();
    change_edible_cleaned_weight();
});
