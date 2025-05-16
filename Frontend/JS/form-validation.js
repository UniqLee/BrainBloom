document.addEventListener('DOMContentLoaded', function () {
    const signUpForm = document.querySelector('form[action="education-selection.html"]');
    const loginForm = document.querySelector('form[action="features.html"]');

    function validateForm(event) {
        event.preventDefault(); // Prevent default form submission
        
        const form = event.target;
        let isValid = true;

        // Validate required fields
        form.querySelectorAll('input[required]').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                alert(`Please fill in the ${input.name} field.`);
            }
        });

        // Validate email format
        const emailInput = form.querySelector('input[type="email"]');
        if (emailInput && !emailInput.value.match(/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/)) {
            isValid = false;
            alert("Please enter a valid email address.");
        }

        // Validate password match (Sign-Up Page)
        const passwordInput = form.querySelector('input[id="password"]');
        const confirmPasswordInput = form.querySelector('input[id="confirmPassword"]');
        if (passwordInput && confirmPasswordInput && passwordInput.value !== confirmPasswordInput.value) {
            isValid = false;
            alert("Passwords do not match.");
        }

        if (isValid) {
            form.submit(); // Submit only if validation passes
        }
    }

    // Apply validation to forms
    if (signUpForm) signUpForm.addEventListener('submit', validateForm);
    if (loginForm) loginForm.addEventListener('submit', validateForm);
});