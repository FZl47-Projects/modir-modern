// Move menubar on click
const toggleBtn = document.querySelector('.menu-toggle-btn');
const sidebar = document.querySelector('.menu-fixed-right');

toggleBtn.addEventListener('click', function () {
    if (toggleBtn.style.right === '250px') {
        toggleBtn.style.right = '0';
        sidebar.style.right = '-300px';
    } else {
        toggleBtn.style.right = '250px';
        sidebar.style.right = '0';
    }
})

let computedStyle = window.getComputedStyle(toggleBtn);
if (computedStyle.getPropertyValue('display') !== 'none') {
    document.onclick = function (e) {
        if (!sidebar.contains(e.target) && !e.target.classList.contains('menu')) {
            toggleBtn.style.right = '0';
            sidebar.style.right = '-300px';
        }
    }
}
