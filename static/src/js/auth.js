

  

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.fiscal-auth-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                e.preventDefault();
                showAlert('Veuillez remplir tous les champs', 'danger');
                return false;
            }
            
            if (!isValidEmail(email)) {
                e.preventDefault();
                showAlert('Format d\'email invalide', 'danger');
                return false;
            }
            
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Connexion...';
        });
    }
});

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type) {
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const form = document.querySelector('.fiscal-auth-form');
    form.parentNode.insertBefore(alertDiv, form);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}


window.addEventListener('load', function() {
    const authCard = document.querySelector('.fiscal-auth-card');
    if (authCard) {
        authCard.style.opacity = '0';
        authCard.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            authCard.style.transition = 'all 0.6s ease';
            authCard.style.opacity = '1';
            authCard.style.transform = 'translateY(0)';
        }, 100);
    }
});

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

document.addEventListener('DOMContentLoaded', function() {
    const error = getUrlParameter('error');
    const message = getUrlParameter('message');
    
    if (error) {
        showAlert(error, 'danger');
    }
    
    if (message) {
        showAlert(message, 'success');
    }
});

setTimeout(function () {
    const alert = document.getElementById('success-alert');
    if (alert) {
        alert.remove();
    }
}, 5000);