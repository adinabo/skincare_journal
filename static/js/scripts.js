// Navbar shrink function
function navbarShrink() {
    const navbarCollapsible = document.querySelector('.nav-wrapper');
    if (!navbarCollapsible) {
        return;
    }
    if (window.scrollY === 0) {
        navbarCollapsible.classList.remove('navbar-shrink');
    } else {
        navbarCollapsible.classList.add('navbar-shrink');
    }
}

// Form Submission Handler
function handleFormSubmit(formId, fetchUrl, redirectUrl, messageId) {
    document.getElementById(formId).addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        const formData = new FormData(this);

        fetch(fetchUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById(messageId);
            if (data.success) {
                window.location.href = redirectUrl;
            } else {
                messageElement.textContent = 'Submission failed: ' + data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById(messageId).textContent = 'An error occurred. Please try again.';
        });
    });
}

// Initialize Materialize Components
document.addEventListe
