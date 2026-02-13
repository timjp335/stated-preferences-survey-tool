// Frontend validation and interaction logic for SP Survey Tool

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Choice card interactions
    const choiceCards = document.querySelectorAll('.choice-card');
    choiceCards.forEach(card => {
        card.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                // Remove selected class from all cards
                choiceCards.forEach(c => c.classList.remove('selected'));
                // Add selected class to this card
                this.classList.add('selected');
            }
        });
    });
    
    // Likert scale interactions
    const likertOptions = document.querySelectorAll('.likert-option label');
    likertOptions.forEach(label => {
        label.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input) {
                input.checked = true;
            }
        });
    });
    
    // Smooth scrolling for better UX
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Add animation class to cards on load
    setTimeout(() => {
        const cards = document.querySelectorAll('.choice-card, .info-box, .form-group');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.5s, transform 0.5s';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 50);
            }, index * 50);
        });
    }, 100);
});

function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value || (field.type === 'radio' && !isRadioGroupChecked(field.name))) {
            isValid = false;
            highlightError(field);
        }
    });
    
    if (!isValid) {
        alert('Bitte füllen Sie alle Pflichtfelder aus.');
    }
    
    return isValid;
}

function isRadioGroupChecked(groupName) {
    const radios = document.querySelectorAll(`input[name="${groupName}"]`);
    return Array.from(radios).some(radio => radio.checked);
}

function highlightError(field) {
    field.style.borderColor = '#ef4444';
    setTimeout(() => {
        field.style.borderColor = '';
    }, 3000);
}

// Helper function for choice selection
function selectChoice(choiceId) {
    const radio = document.getElementById('choice_' + choiceId);
    if (radio) {
        radio.checked = true;
        
        // Visual feedback
        const cards = document.querySelectorAll('.choice-card');
        cards.forEach(card => card.classList.remove('selected'));
        
        const selectedCard = radio.closest('.choice-card');
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    }
}

// Make selectChoice available globally
window.selectChoice = selectChoice;
