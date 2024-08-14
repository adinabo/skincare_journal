/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
// login form 
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);

    fetch('/login', {  // Replace with your actual login route
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const loginMessage = document.getElementById('loginMessage');
        if (data.success) {
            // Redirect to the user's profile or homepage
            window.location.href = '/profile';  // Replace with the actual redirect route
        } else {
            // Display error message
            loginMessage.textContent = 'Login failed: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loginMessage').textContent = 'An error occurred. Please try again.';
    });
});

// register form 
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);

    fetch('/register', {  // Replace with your actual register route
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const registerMessage = document.getElementById('registerMessage');
        if (data.success) {
            // Redirect to login page or user's profile
            window.location.href = '/login';  // Replace with the actual redirect route
        } else {
            // Display error message
            registerMessage.textContent = 'Registration failed: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('registerMessage').textContent = 'An error occurred. Please try again.';
    });
});
