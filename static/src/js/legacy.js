document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuToggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
    }

    // Close menu when a link is clicked
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks && navLinks.classList.remove('active');
            const icon = mobileMenuBtn && mobileMenuBtn.querySelector('i');
            if (icon) icon.className = 'fas fa-bars';
        });
    });

    // 2. Sticky Navbar Effect on Scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
            navbar.style.background = 'rgba(0, 15, 54, 0.98)'; // Dark navy blue
        } else {
            navbar.style.boxShadow = ''; // Reset to CSS default
            navbar.style.background = ''; // Reset to CSS default
        }
    });

    // 3. Login Form Demo Submission
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent page reload
            const btn = loginForm.querySelector('.btn-login');
            const originalText = btn.innerHTML;
            
            // Show loading state
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
            
            // Simulate API call
            setTimeout(() => {
                alert('Success! This is a demo template. Backend integration is required for real login.');
                btn.innerHTML = originalText;
            }, 1500);
        });
    }

    // 4. Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        // Check local storage for preference
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-mode');
            darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }

        darkModeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
                darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                localStorage.setItem('darkMode', null);
                darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            }
        });
    }

    // 5. Bookmark Interactions
    const bookmarkBtns = document.querySelectorAll('.bookmark-btn');
    bookmarkBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = 'var(--secondary)';
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = 'var(--text-muted)';
            }
        });
    });

    // 6. WhatsApp Floating Button (Global)
    const waButtonHTML = `
        <a href="https://whatsapp.com/channel/0029VbD3NvLKLaHszgpIiI29" target="_blank" rel="noopener noreferrer" class="whatsapp-float">
            <span class="wa-cta">👉 Join WhatsApp Channel</span>
            <div class="wa-icon-wrapper">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width: 55px; height: 55px;">
            </div>
        </a>
    `;
    document.body.insertAdjacentHTML('beforeend', waButtonHTML);

    // 7. Premium Typewriter Animation
    const twTextElement = document.getElementById('typewriter-text');
    if (twTextElement) {
        const phrases = [
            "✨ Crack UPSC with Confidence",
            "✨ Learn Smarter. Achieve Faster.",
            "✨ Daily News. Daily Success.",
            "✨ Build Strong Basics. Reach Your Goals.",
            "✨ One Platform. Every Subject.",
            "✨ Stay Updated. Stay Ahead.",
            "✨ Master Every Subject, One Step at a Time.",
            "✨ Learn Today. Lead Tomorrow.",
            "✨ Smart Learning for Smart Aspirants.",
            "✨ Your Success Starts with THE BASICS."
        ];
        
        let phraseIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        const typeEffect = () => {
            const currentPhrase = phrases[phraseIndex];
            
            if (isDeleting) {
                twTextElement.textContent = currentPhrase.substring(0, charIndex - 1);
                charIndex--;
            } else {
                twTextElement.textContent = currentPhrase.substring(0, charIndex + 1);
                charIndex++;
            }
            
            // Speed: 70-90 ms
            let typeSpeed = Math.floor(Math.random() * (90 - 70 + 1)) + 70;
            
            if (isDeleting) {
                typeSpeed /= 2; // Delete faster
            }
            
            if (!isDeleting && charIndex === currentPhrase.length) {
                // Pause for 3 seconds before deleting
                typeSpeed = 3000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                phraseIndex = (phraseIndex + 1) % phrases.length;
                typeSpeed = 500; // Small pause before next word
            }
            
            setTimeout(typeEffect, typeSpeed);
        };
        
        setTimeout(typeEffect, 500);
    }
});
