/**
 * Simple SPA Routing System
 */
const pages = ['home', 'service-owned', 'service-management', 'service-sns', 'about', 'contact'];

function navigate(pageId) {
    // Validate page
    if (!pages.includes(pageId)) return;

    // Hide all pages
    pages.forEach(id => {
        const el = document.getElementById(`page-${id}`);
        if (el) {
            el.classList.remove('active');
        }
    });

    // Show selected page
    const targetPage = document.getElementById(`page-${pageId}`);
    if (targetPage) {
        targetPage.classList.add('active');
        // Scroll to top smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Update URL hash for simple back-button support (optional but good practice)
    window.location.hash = pageId;
}

// Handle initial load based on URL hash
window.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash.replace('#', '');
    if (hash && pages.includes(hash)) {
        navigate(hash);
    } else {
        navigate('home');
    }
});

// Handle browser back/forward buttons
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '');
    if (hash && pages.includes(hash)) {
        navigate(hash);
    } else if (!hash) {
        navigate('home');
    }
});


/**
 * Mobile Menu Toggle
 */
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const menuIcon = document.getElementById('menu-icon');

function toggleMobileMenu() {
    mobileMenu.classList.toggle('hidden');
    if (mobileMenu.classList.contains('hidden')) {
        menuIcon.classList.remove('ph-x');
        menuIcon.classList.add('ph-list');
    } else {
        menuIcon.classList.remove('ph-list');
        menuIcon.classList.add('ph-x');
    }
}

mobileMenuBtn.addEventListener('click', toggleMobileMenu);

/**
 * Header Scroll Effect (Glassmorphism shadow adjust)
 */
const header = document.getElementById('main-header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        header.classList.add('shadow-sm');
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    } else {
        header.classList.remove('shadow-sm');
        header.style.background = 'rgba(255, 255, 255, 0.85)';
    }
});
