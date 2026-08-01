'use strict'

const radioButtonBand = document.getElementById('looking_for-0');
const radioButtonMusician = document.getElementById('looking_for-1');
const formLabels = document.getElementsByClassName('form-label');



radioButtonBand.addEventListener('change', function () {
    formLabels[1].innerHTML = 'Ik ben een:';
})
radioButtonMusician.addEventListener('change', function () {
    formLabels[1].innerHTML = 'Ik zoek een:'
})