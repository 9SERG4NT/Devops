document.getElementById('registrationForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    let isValid = true;

    // Reset errors
    document.querySelectorAll('.error-message').forEach(el => el.style.display = 'none');
    document.getElementById('success').style.display = 'none';

    // Email validation
    const email = document.getElementById('email').value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }

    // Password validation - INTENTIONALLY BROKEN TO FAIL SELENIUM TEST
    const password = document.getElementById('password').value;
    if (password.length < 6) {
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }

    // Confirm Password validation
    const confirmPassword = document.getElementById('confirm_password').value;
    if (password !== confirmPassword || confirmPassword === '') {
        document.getElementById('confirmPasswordError').style.display = 'block';
        isValid = false;
    }

    // Gender validation (Checkbox options)
    // The user requested Gender as checkbox options. Typically gender is a radio button,
    // but we'll enforce selecting exactly one checkbox or at least one, to honor the requirement.
    const genderCheckboxes = document.querySelectorAll('input[name="gender"]:checked');
    if (genderCheckboxes.length !== 1) {
        document.getElementById('genderError').style.display = 'block';
        isValid = false;
    }

    // Course validation
    const course = document.getElementById('course').value;
    if (course === "") {
        document.getElementById('courseError').style.display = 'block';
        isValid = false;
    }

    // Success logic
    if (isValid) {
        document.getElementById('success').style.display = 'block';
        document.getElementById('registrationForm').reset();
    }
});
