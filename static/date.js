'use strict';

const advertisements = document.querySelectorAll('.card');

for (const ad of advertisements) {
    const h3Element = ad.querySelector('h3');
    const h3Array = h3Element.textContent.split(',');
    let dateArray = h3Array[0];
    dateArray = dateArray.split('-');
    console.log(dateArray[0]);
    h3Element.textContent = `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}, ${h3Array[1]}`
}

