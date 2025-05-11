// Main JavaScript file for Hồ Hằng shop

// Initialize tooltips
const initTooltips = () => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
};

// Handle quantity input changes
const setupQuantityControls = () => {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    quantityInputs.forEach(input => {
        const minusBtn = input.parentElement.querySelector('.btn-minus');
        const plusBtn = input.parentElement.querySelector('.btn-plus');
        
        // Set min value to 1
        input.addEventListener('change', () => {
            if (parseInt(input.value) < 1) {
                input.value = 1;
            }
        });
        
        // Decrease quantity
        if (minusBtn) {
            minusBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value);
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    // Trigger change event to update forms
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
        
        // Increase quantity
        if (plusBtn) {
            plusBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value);
                input.value = currentValue + 1;
                // Trigger change event to update forms
                input.dispatchEvent(new Event('change'));
            });
        }
    });
};

// Auto-submit quantity update form on change
const setupAutoSubmit = () => {
    const quantityForms = document.querySelectorAll('.update-cart-form');
    
    quantityForms.forEach(form => {
        const input = form.querySelector('.quantity-input');
        if (input) {
            input.addEventListener('change', () => {
                form.submit();
            });
        }
    });
};

// Close alerts automatically after 5 seconds
const setupAutoCloseAlerts = () => {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initTooltips();
    setupQuantityControls();
    setupAutoSubmit();
    setupAutoCloseAlerts();
});