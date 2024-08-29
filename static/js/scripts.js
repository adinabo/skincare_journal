// Navbar shrink function from Materialize
function navbarShrink() {
    const navbarCollapsible = document.querySelector(".nav-wrapper");
    if (!navbarCollapsible) return;

    if (window.scrollY === 0) {
        navbarCollapsible.classList.remove("navbar-shrink");
    } else {
        navbarCollapsible.classList.add("navbar-shrink");
    }
}

// Form Submission Handler
function handleFormSubmit(formId, fetchUrl, redirectUrl, messageId) {
    document.getElementById(formId).addEventListener("submit", function(event) {
        event.preventDefault(); 

        const formData = new FormData(this);

        fetch(fetchUrl, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById(messageId);
            if (data.success) {
                window.location.href = redirectUrl;
            } else {
                messageElement.textContent =
                 "Submission failed: " + data.message;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById(messageId).textContent
             = "An error occurred. Please try again.";
        });
    });
}

// Consolidated DOMContentLoaded Event Listener
document.addEventListener("DOMContentLoaded", function() {
    // Initialize Sidenav
    var sidenavElems = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenavElems);

    // Initialize Selects
    var selectElems = document.querySelectorAll("select");
    M.FormSelect.init(selectElems);

    // Initialize Modals
    var modalElems = document.querySelectorAll(".modal");
    M.Modal.init(modalElems);

    // Initialize Collapsible
    var collapsibleElems = document.querySelectorAll(".collapsible");
    M.Collapsible.init(collapsibleElems, {
        accordion: false
    });

    // Profile Page: Filter Products Based on Skincare Step
    var skincareStepSelect = document.getElementById("skincare_step");
    var productNameSelect = document.getElementById("product_name");

    if (skincareStepSelect && productNameSelect) {
        skincareStepSelect.addEventListener("change", function() {
            var selectedStep = skincareStepSelect.value;

            for (var i = 0; i < productNameSelect.options.length; i++) {
                var option = productNameSelect.options[i];
                option.style.display= option.getAttribute("data-type")
                 === selectedStep ? "" : "none";
            }
            // Reset the product name select
            productNameSelect.selectedIndex = 0;
            M.FormSelect.init(productNameSelect);
        });
    }
});
