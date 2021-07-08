var menu = document.querySelector('#header__menu');
var main = document.querySelector('main');
var drawer = document.querySelector('.nav');

menu.addEventListener('click', function(e) {
  drawer.classList.toggle('open');
  main.classList.toggle('open')
  e.stopPropagation();
});