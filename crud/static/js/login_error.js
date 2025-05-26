document.addEventListener("DOMContentLoaded", function() {
    const hasError = window.location.search.includes("error") ||
                        document.querySelector('[data-django-messages]')||
                        textContent.includes("Invalid");

if (hasError) {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginError = document.createElement('div');


    usernameInput.style.borderColor = 'ef4444';
    passwordInput.style.borderColor = 'ef4444';

    
});