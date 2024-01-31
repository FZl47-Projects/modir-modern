// Move menubar on click
const toggleBtn = document.querySelector('.menu-toggle-btn');
const toggleCloseBtn = document.querySelector('.menu-toggle-btn-close');
const sidebar = document.querySelector('.menu-fixed-right');

toggleBtn.addEventListener('click', function () {
    sidebar.style.right = '0';
})

toggleCloseBtn.addEventListener('click', function () {
    sidebar.style.right = '-300px';
})

let computedStyle = window.getComputedStyle(toggleBtn);
if (computedStyle.getPropertyValue('display') !== 'none') {
    document.onclick = function (e) {
        if (!sidebar.contains(e.target) && !e.target.classList.contains('menu')) {
            sidebar.style.right = '-300px';
        }
    }
}
