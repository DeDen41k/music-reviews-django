// navigation.js
function toggleMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    toggle.classList.toggle('active');
    navLinks.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const nav = document.querySelector('nav');
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (!nav.contains(event.target)) {
        toggle.classList.remove('active');
        navLinks.classList.remove('active');
    }
});

// Add scroll effect to navigation
window.addEventListener('scroll', function() {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.backdropFilter = 'blur(25px)';
        nav.style.background = 'linear-gradient(145deg, rgba(45, 37, 32, 0.95) 0%, rgba(58, 51, 43, 0.95) 100%)';
    } else {
        nav.style.backdropFilter = 'blur(20px)';
        nav.style.background = 'linear-gradient(145deg, var(--surface-color) 0%, var(--surface-light) 100%)';
    }
});