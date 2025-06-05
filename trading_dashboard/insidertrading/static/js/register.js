document.addEventListener('DOMContentLoaded', function () {
    // Password toggles
    const passwordToggle = document.getElementById('passwordToggle');
    const confirmPasswordToggle = document.getElementById('confirmPasswordToggle');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirmPassword');

    // Form fields for validation
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const phoneInput = document.getElementById('phone');
    const countrySelect = document.getElementById('country');
    const termsCheckbox = document.getElementById('termsAgreement');

    // Error messages
    const usernameError = document.getElementById('username-error');
    const emailError = document.getElementById('email-error');
    const confirmPasswordError = document.getElementById('confirm-password-error');
    const firstNameError = document.getElementById('first-name-error');
    const lastNameError = document.getElementById('last-name-error');
    const phoneError = document.getElementById('phone-error');
    const countryError = document.getElementById('country-error');
    const termsError = document.getElementById('terms-error');

    // Success message
    const successMessage = document.getElementById('successMessage');
    const createAccountBtn = document.getElementById('createAccountBtn');

    // Password strength elements
    const strengthMeter = document.getElementById('strengthMeter');
    const passwordFeedback = document.getElementById('passwordFeedback');
    const reqLength = document.getElementById('req-length');
    const reqUppercase = document.getElementById('req-uppercase');
    const reqLowercase = document.getElementById('req-lowercase');
    const reqNumber = document.getElementById('req-number');
    const reqSpecial = document.getElementById('req-special');

    // Password visibility toggles
    passwordToggle.addEventListener('click', function () {
        togglePasswordVisibility(passwordField, this);
    });

    confirmPasswordToggle.addEventListener('click', function () {
        togglePasswordVisibility(confirmPasswordField, this);
    });

    function togglePasswordVisibility(field, toggle) {
        const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
        field.setAttribute('type', type);

        // Toggle icon
        toggle.querySelector('i').classList.toggle('fa-eye');
        toggle.querySelector('i').classList.toggle('fa-eye-slash');
    }

    // Password strength checker
    passwordField.addEventListener('input', function () {
        checkPasswordStrength(this.value);

        // Check if passwords match whenever password changes
        if (confirmPasswordField.value) {
            checkPasswordsMatch();
        }
    });

    confirmPasswordField.addEventListener('input', checkPasswordsMatch);

    function checkPasswordStrength(password) {
        // Reset requirements
        reqLength.classList.remove('met');
        reqUppercase.classList.remove('met');
        reqLowercase.classList.remove('met');
        reqNumber.classList.remove('met');
        reqSpecial.classList.remove('met');

        // Update icons
        document.querySelectorAll('.requirement').forEach(req => {
            req.querySelector('i').className = 'far fa-circle';
        });

        // Check requirements
        let strength = 0;

        // Length check
        if (password.length >= 8) {
            strength += 20;
            reqLength.classList.add('met');
            reqLength.querySelector('i').className = 'fas fa-check-circle';
        }

        // Uppercase check
        if (/[A-Z]/.test(password)) {
            strength += 20;
            reqUppercase.classList.add('met');
            reqUppercase.querySelector('i').className = 'fas fa-check-circle';
        }

        // Lowercase check
        if (/[a-z]/.test(password)) {
            strength += 20;
            reqLowercase.classList.add('met');
            reqLowercase.querySelector('i').className = 'fas fa-check-circle';
        }

        // Number check
        if (/[0-9]/.test(password)) {
            strength += 20;
            reqNumber.classList.add('met');
            reqNumber.querySelector('i').className = 'fas fa-check-circle';
        }

        // Special character check
        if (/[^A-Za-z0-9]/.test(password)) {
            strength += 20;
            reqSpecial.classList.add('met');
            reqSpecial.querySelector('i').className = 'fas fa-check-circle';
        }

        // Update strength meter and feedback
        strengthMeter.style.width = strength + '%';

        // Color coding
        if (strength < 40) {
            strengthMeter.style.backgroundColor = '#e74c3c';
            passwordFeedback.textContent = 'Weak password';
            passwordFeedback.style.color = '#e74c3c';
        } else if (strength < 80) {
            strengthMeter.style.backgroundColor = '#f39c12';
            passwordFeedback.textContent = 'Moderate password';
            passwordFeedback.style.color = '#f39c12';
        } else {
            strengthMeter.style.backgroundColor = '#2ecc71';
            passwordFeedback.textContent = 'Strong password';
            passwordFeedback.style.color = '#2ecc71';
        }
    }

    function checkPasswordsMatch() {
        if (passwordField.value !== confirmPasswordField.value) {
            confirmPasswordError.style.display = 'block';
            return false;
        } else {
            confirmPasswordError.style.display = 'none';
            return true;
        }
    }

    // Form submission
    document.getElementById('signupForm').addEventListener('submit', function (e) {

        // Perform all validations at once
        let isValid = true;

        // Reset all error messages
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(msg => msg.style.display = 'none');

        // Validate username
        if (usernameInput.value.length < 4) {
            usernameError.style.display = 'block';
            isValid = false;
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
            emailError.style.display = 'block';
            isValid = false;
        }

        // Validate password strength
        const hasMinLength = passwordField.value.length >= 8;
        const hasUpperCase = /[A-Z]/.test(passwordField.value);
        const hasLowerCase = /[a-z]/.test(passwordField.value);
        const hasNumber = /[0-9]/.test(passwordField.value);
        const hasSpecialChar = /[^A-Za-z0-9]/.test(passwordField.value);

        if (!(hasMinLength && hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar)) {
            isValid = false;
        }

        // Validate password match
        if (passwordField.value !== confirmPasswordField.value) {
            confirmPasswordError.style.display = 'block';
            isValid = false;
        }

        // Validate personal information
        if (firstNameInput.value.trim() === '') {
            firstNameError.style.display = 'block';
            isValid = false;
        }

        if (lastNameInput.value.trim() === '') {
            lastNameError.style.display = 'block';
            isValid = false;
        }


        // Validate phone
        const phoneRegex = /^\d{10,15}$/;
        if (!phoneRegex.test(phoneInput.value.replace(/[^0-9]/g, ''))) {
            phoneError.style.display = 'block';
            isValid = false;
        }


        // Validate country selection
        if (!countrySelect.value) {
            countryError.style.display = 'block';
            isValid = false;
        }


        // Validate terms agreement
        if (!termsCheckbox.checked) {
            termsError.style.display = 'block';
            isValid = false;
        }


        // If not valid, scroll to the first error
        if (!isValid) {
            const firstError = document.querySelector('.error-message[style="display: block"]');
            if (firstError) {
                firstError.parentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            console.log('Form submission prevented due to validation errors.');
            e.preventDefault();
            return;
        }

        this.submit();

    });
});