// Main JavaScript file for the Shop Online E-commerce Site

document.addEventListener('DOMContentLoaded', function() {
    
    // Bootstrap Tooltips Initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-important)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Product quantity input handling
    setupQuantityInputs();
    
    // Review star rating visual logic
    setupStarRatings();
    
    // Product image zoom effect on hover
    setupProductImageZoom();
    
    // Form validation enhancement
    setupFormValidation();
});

/**
 * Sets up event handlers for quantity adjustment buttons
 */
function setupQuantityInputs() {
    // Quantity increment and decrement is handled directly in the templates
    // But we can add additional validation or formatters here
    
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Ensure the value is at least 1
            if (this.value < 1) {
                this.value = 1;
            }
            
            // Optional: Update any related price calculations
            updateItemPrices(this);
        });
    });
}

/**
 * Updates item prices in the cart when quantity changes
 * This is a placeholder function that could be implemented if needed
 */
function updateItemPrices(quantityInput) {
    // This would be implemented if we want to update totals dynamically
    // without reloading the page. Currently handled by the server.
}

/**
 * Sets up interactive star ratings for product reviews
 */
function setupStarRatings() {
    const ratingSelects = document.querySelectorAll('select[name="rating"]');
    
    ratingSelects.forEach(select => {
        // When the rating select changes, update any visual star display if needed
        select.addEventListener('change', function() {
            const rating = parseInt(this.value);
            const starContainer = this.closest('form').querySelector('.star-display');
            
            if (starContainer) {
                starContainer.innerHTML = '';
                
                // Create stars based on selected rating
                for (let i = 1; i <= 5; i++) {
                    const star = document.createElement('i');
                    
                    if (i <= rating) {
                        star.className = 'fas fa-star text-warning';
                    } else {
                        star.className = 'far fa-star text-warning';
                    }
                    
                    starContainer.appendChild(star);
                    starContainer.appendChild(document.createTextNode(' '));
                }
            }
        });
    });
}

/**
 * Sets up zoom effect on product images
 */
function setupProductImageZoom() {
    const productImages = document.querySelectorAll('.product-detail-image');
    
    productImages.forEach(img => {
        img.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
            this.style.cursor = 'zoom-in';
        });
        
        img.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

/**
 * Enhances form validation with custom feedback
 */
function setupFormValidation() {
    // Add custom validation for forms with the 'needs-validation' class
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password strength meter (if password fields exist)
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        field.addEventListener('input', function() {
            // Simple password strength checker
            const password = this.value;
            const strengthMeter = this.parentElement.querySelector('.password-strength');
            
            if (strengthMeter) {
                if (password.length < 8) {
                    strengthMeter.innerHTML = '<span class="text-danger">Yếu</span>';
                } else if (password.length < 12) {
                    strengthMeter.innerHTML = '<span class="text-warning">Trung bình</span>';
                } else {
                    strengthMeter.innerHTML = '<span class="text-success">Mạnh</span>';
                }
            }
        });
    });
}

/**
 * Handles the tab switching in product details and profile pages
 */
function openTab(evt, tabName) {
    // Hide all tab content
    const tabContent = document.getElementsByClassName('tab-pane');
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
    }
    
    // Remove 'active' class from all tab buttons
    const tabLinks = document.getElementsByClassName('nav-link');
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(' active', '');
    }
    
    // Show the current tab and add 'active' class to the button
    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';
}
