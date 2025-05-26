document.addEventListener("DOMContentLoaded", function() {
    const hasError = window.location.search.includes("error") ||
                        document.querySelector('[data-django-messages]')||
                        textContent.includes("Invalid");

    if (hasError) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const loginError = document.createElement('loginError');


        usernameInput.style.borderColor = 'ef4444';
        passwordInput.style.borderColor = 'ef4444';

        loginError.classList.remove('hidden');

        function clearError() {
            usernameInput.style.borderColor = '';
            passwordInput.style.borderColor = '';
            loginError.classList.add('hidden');
    }

    usernameInput.addEventListener('input', clearError);
    passwordInput.addEventListener('input', clearError);

    }
    
});