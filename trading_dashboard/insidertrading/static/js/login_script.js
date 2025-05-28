document.addEventListener('DOMContentLoaded', function () {
    // Password visibility toggle
    const passwordToggle = document.getElementById('passwordToggle');
    const passwordField = document.getElementById('password');

    if (passwordToggle) {
        passwordToggle.addEventListener('click', function () {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);

            // Toggle icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            }
        });
    }

    // Simple form validation (client-side only)
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('username-error');
    const passwordError = document.getElementById('password-error');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            let isValid = true;

            // Reset error messages
            usernameError.style.display = 'none';
            passwordError.style.display = 'none';

            // Validate username
            if (usernameInput.value.trim() === '') {
                usernameError.style.display = 'block';
                isValid = false;
            }

            // Validate password
            if (passwordInput.value.length < 6) {
                passwordError.style.display = 'block';
                isValid = false;
            }

            // If form is invalid, prevent submission
            if (!isValid) {
                e.preventDefault();
            }
        
        });
    }
});