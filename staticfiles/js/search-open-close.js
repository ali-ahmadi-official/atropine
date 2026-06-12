/*====================
  Searchbar open/close Js
======================*/
const searchBtn = document.querySelector('.search-button');
const searchPanel = document.querySelector('.search-box');
const closeSearch = document.querySelector('.close-search');
searchBtn.onclick = function () {
    searchPanel.classList.add('show');
};
closeSearch.onclick = function () {
    searchPanel.classList.remove('show');
};