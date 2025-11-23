// Portfolio Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initNavigation();
    initAnimations();
    initInteractiveElements();
    initThemeToggle();
    
    console.log('Portfolio website loaded successfully! 🚀');
});

// Navigation Enhancement
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Add active class to current page nav link
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(33, 37, 41, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.backgroundColor = '';
            navbar.style.backdropFilter = '';
        }
    });
    
    // Mobile menu close on link click
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
}

// Animation System
function initAnimations() {
    // Intersection Observer for scroll animations
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe all cards and sections
    const animateElements = document.querySelectorAll('.card, .hero-section, .features-section .col-md-4');
    animateElements.forEach(el => {
        animationObserver.observe(el);
    });
    
    // Staggered animation for card grids
    const cardGrids = document.querySelectorAll('.row .col-md-4, .row .col-md-6');
    cardGrids.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Interactive Elements
function initInteractiveElements() {
    // Enhanced card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.1)';
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // Button ripple effect
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255,255,255,0.6);
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Theme Toggle (Optional Dark Mode)
function initThemeToggle() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const initialTheme = savedTheme || systemTheme;
    
    document.documentElement.setAttribute('data-theme', initialTheme);
    
    // Create theme toggle button (if not exists)
    if (!document.querySelector('.theme-toggle')) {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'btn btn-outline-secondary btn-sm theme-toggle position-fixed';
        themeToggle.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px;';
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        themeToggle.setAttribute('aria-label', 'Toggle dark mode');
        
        themeToggle.addEventListener('click', toggleTheme);
        document.body.appendChild(themeToggle);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    const themeToggle = document.querySelector('.theme-toggle i');
    themeToggle.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    
    // Add transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

// Loading Screen
function showLoadingScreen() {
    const loading = document.createElement('div');
    loading.className = 'loading-screen';
    loading.innerHTML = `
        <div class="loading-content">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading your portfolio...</p>
        </div>
    `;
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.9);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    `;
    
    document.body.appendChild(loading);
    
    setTimeout(() => {
        loading.style.opacity = '0';
        loading.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            loading.remove();
        }, 500);
    }, 1000);
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let lastFunc;
    let lastRan;
    return function(...args) {
        if (!lastRan) {
            func.apply(this, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(() => {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(this, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

// Page-specific functionality
const PageHandlers = {
    // Home page animations
    home: function() {
        const heroText = document.querySelector('.hero-text');
        if (heroText) {
            heroText.style.animation = 'fadeInUp 1s ease-out';
        }
        
        const featureCards = document.querySelectorAll('.features-section .card');
        featureCards.forEach((card, index) => {
            card.style.animationDelay = `${0.2 + index * 0.1}s`;
            card.classList.add('fade-in');
        });
    },
    
    // Steam page interactions
    steam: function() {
        const gameCards = document.querySelectorAll('.game-card');
        gameCards.forEach(card => {
            card.addEventListener('click', function() {
                this.style.animation = 'pulse 0.5s ease';
                setTimeout(() => {
                    this.style.animation = '';
                }, 500);
            });
        });
    },
    
    // Music page controls
    music: function() {
        const playButtons = document.querySelectorAll('.music-controls .btn');
        playButtons.forEach(button => {
            button.addEventListener('click', function() {
                const icon = this.querySelector('i');
                if (icon.classList.contains('fa-play')) {
                    icon.classList.remove('fa-play');
                    icon.classList.add('fa-pause');
                } else {
                    icon.classList.remove('fa-pause');
                    icon.classList.add('fa-play');
                }
            });
        });
    },
    
    // Diary page enhancements
    diary: function() {
        const entries = document.querySelectorAll('.diary-entry');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'slideIn 0.6s ease-out';
                }
            });
        }, { threshold: 0.2 });
        
        entries.forEach(entry => observer.observe(entry));
    }
};

// Initialize page-specific handlers
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    const page = path === '/' ? 'home' : path.substring(1).replace('-', '');
    
    if (PageHandlers[page]) {
        PageHandlers[page]();
    }
});

// Performance monitoring
const performanceObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (entry.entryType === 'navigation') {
            console.log(`Page load time: ${entry.loadEventEnd - entry.loadEventStart}ms`);
        }
    }
});

try {
    performanceObserver.observe({ entryTypes: ['navigation'] });
} catch (e) {
    console.log('Performance Observer not supported');
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('Portfolio error:', event.error);
    // Could send error reports to analytics here
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-theme="dark"] {
        --bs-body-bg: #121212;
        --bs-body-color: #e0e0e0;
    }
    
    [data-theme="dark"] .card {
        background-color: #1e1e1e !important;
        color: #e0e0e0;
    }
    
    [data-theme="dark"] .bg-light {
        background-color: #2c2c2c !important;
    }
    
    [data-theme="dark"] .text-muted {
        color: #adb5bd !important;
    }
    
    .loading-screen .loading-content {
        text-align: center;
    }
`;
document.head.appendChild(style);

// Export for use in other scripts if needed
window.PortfolioJS = {
    PageHandlers,
    toggleTheme,
    debounce,
    throttle
};

// Mobile-Specific Enhancements
(function() {
    'use strict';
    
    // Detect if user is on mobile device
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    if (isMobile || isTouch) {
        document.body.classList.add('mobile-device');
        
        // Fix Bootstrap dropdown behavior on mobile
        document.addEventListener('DOMContentLoaded', function() {
            // Enhanced dropdown handling for mobile
            const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
            
            dropdownToggles.forEach(toggle => {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const dropdown = this.nextElementSibling;
                    const parentItem = this.closest('.dropdown');
                    
                    // Close other dropdowns
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        if (menu !== dropdown) {
                            menu.classList.remove('show');
                        }
                    });
                    
                    // Toggle current dropdown
                    dropdown.classList.toggle('show');
                });
            });
            
            // Close dropdowns when clicking outside on mobile
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.dropdown')) {
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        menu.classList.remove('show');
                    });
                }
            });
            
            // Prevent dropdown from closing when clicking inside on mobile
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
            
            // Close mobile menu after clicking a link
            const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)');
            const navbarCollapse = document.querySelector('.navbar-collapse');
            const navbarToggler = document.querySelector('.navbar-toggler');
            
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                });
            });
            
            // Close navbar when clicking outside on mobile
            document.addEventListener('click', function(e) {
                if (window.innerWidth < 992) {
                    const isClickInsideNav = e.target.closest('.navbar');
                    if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                }
            });
        });
        
        // Prevent zoom on input focus for iOS
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                if (this.style.fontSize !== '16px') {
                    this.style.fontSize = '16px';
                }
            });
        });
        
        // Add touch feedback to buttons
        const buttons = document.querySelectorAll('.btn, button');
        buttons.forEach(button => {
            button.addEventListener('touchstart', function() {
                this.style.opacity = '0.7';
            });
            button.addEventListener('touchend', function() {
                this.style.opacity = '1';
            });
        });
        
        // Smooth scroll behavior for mobile
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        // Close all open dropdowns on orientation change
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
        
        // Close mobile navbar on orientation change
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            const navbarToggler = document.querySelector('.navbar-toggler');
            if (navbarToggler) {
                navbarToggler.click();
            }
        }
    });
    
    // Optimize scroll performance on mobile
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                // Add your scroll-based animations here
                ticking = false;
            });
            ticking = true;
        }
    });
    
})();