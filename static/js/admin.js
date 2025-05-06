document.addEventListener('DOMContentLoaded', function() {
    // Password masking
    const passwordCells = document.querySelectorAll('.password-cell');
    passwordCells.forEach(cell => {
        const input = cell.querySelector('input');
        if (input) {
            const originalPassword = input.getAttribute('data-password');
            if (originalPassword) {
                input.value = '•'.repeat(originalPassword.length);
                const eyeIcon = cell.querySelector('.eye-icon');
                if (eyeIcon) {
                    eyeIcon.textContent = '👁️';
                }
            }
        }
    });

    // Eye icon click handler
    document.querySelectorAll('.eye-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (!input) return;
            
            const currentPassword = input.value;
            const originalPassword = input.getAttribute('data-password');
            
            if (originalPassword && currentPassword.includes('•')) {
                // Show original password
                input.value = originalPassword;
                this.textContent = '👁️';
                this.classList.add('showing');
            } else {
                // Mask password again
                input.value = '•'.repeat(originalPassword.length);
                this.textContent = '👁️';
                this.classList.remove('showing');
            }
        });
    });

    // Auto-hide flash messages with fade-out animation
    const flashMessages = document.querySelectorAll('.flash-message[data-fade="true"]');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => {
                message.style.display = 'none';
            }, 500);
        }, 10000);
    });
});
