// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Add a loading spinner or disable the submit button to prevent multiple submissions
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = 'Submitting...';
        });
    });

    // Add event listeners for radio buttons to highlight selected choice
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            const parentDiv = radio.closest('.form-group');
            const labels = parentDiv.querySelectorAll('label');
            labels.forEach(label => label.classList.remove('selected'));
            const selectedLabel = parentDiv.querySelector(`label[for="${radio.id}"]`);
            selectedLabel.classList.add('selected');
        });
    });
});
