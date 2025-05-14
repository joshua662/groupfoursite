document.addEventListener('DOMContentLoaded', function() {
    const toastMessages = document.querySelectorAll('[role="alert"]');
    
    toastMessages.forEach(toast => {
        const messageContent = toast.querySelector('.ms-3').textContent.trim();
        
        if (messageContent) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';
            toast.style.transition = 'all 0.3s ease-in-out';
            
            setTimeout(() => {
                toast.style.opacity = '1';
                toast.style.transform = 'translateY(0)';
            }, 100);

            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 3000);

            const closeButton = toast.querySelector('[data-dismiss-target]');
            if (closeButton) {
                closeButton.addEventListener('click', () => {
                    toast.style.opacity = '0';
                    toast.style.transform = 'translateY(-10px)';
                    setTimeout(() => {
                        toast.remove();
                    }, 300);
                });
            }
        } else {
            toast.remove();
        }
    });
});