'use strict';

const advertisement = document.querySelector('.card');

if (!advertisement) {
    const h1Div = document.querySelector('.container');
    const noAdsFound = document.createElement('p');
    noAdsFound.textContent = 'No results found :(';
    h1Div.appendChild(noAdsFound)
}