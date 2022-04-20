const activeLink = window.location.href;
let nav_links = document.querySelectorAll('.nav-item.profile a');
nav_links.forEach(function(link) {
    if (link.href == activeLink) {
        link.parentElement.classList.add('active');
    };
});