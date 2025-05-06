document.addEventListener('DOMContentLoaded', function() {
    // Password toggle functionality
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.querySelector('.form-group i');
    
    if (passwordInput && eyeIcon) {
        eyeIcon.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle eye icon classes
            if (type === 'text') {
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }

    // Form validation
    const form = document.querySelector('.login-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields');
                return;
            }

            // Add loading state
            const loginBtn = document.querySelector('.login-btn');
            if (loginBtn) {
                loginBtn.disabled = true;
                loginBtn.style.opacity = '0.7';
            }
        });

        // Remove loading state on error
        form.addEventListener('error', function() {
            const loginBtn = document.querySelector('.login-btn');
            if (loginBtn) {
                loginBtn.disabled = false;
                loginBtn.style.opacity = '1';
            }
        });
    }

    // Input focus effects
    const inputs = document.querySelectorAll('.form-group input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.querySelector('label').classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.querySelector('label').classList.remove('focused');
            }
        });
    });

    // Add animation to form elements
    const formElements = document.querySelectorAll('.form-group, .login-btn, .admin-link');
    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        }, 100 * index);
    });

    // Add smooth scrolling to admin link
    const adminLink = document.querySelector('.admin-link a');
    if (adminLink) {
        adminLink.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            
            // Add loading animation
            const linkIcon = this.querySelector('i');
            linkIcon.style.transform = 'scale(1.2) rotate(360deg)';
            
            setTimeout(() => {
                window.location.href = url;
            }, 300);
        });
    }
});
