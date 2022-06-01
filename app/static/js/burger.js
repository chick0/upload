document.addEventListener('DOMContentLoaded', () => {
    const burgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if (burgers.length > 0) {
        burgers.forEach(function(burger){
            burger.addEventListener('click', () => {
                document.getElementById(burger.dataset.target).classList.toggle('is-active');
            });
        });
    }
});