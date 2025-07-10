// Payment Modal Functions
function openPaymentModal(productId, productName, productPrice) {
    document.getElementById('productName').textContent = productName;
    document.getElementById('productPrice').textContent = productPrice.toFixed(2);
    document.getElementById('paymentForm').action = '/pay/' + productId;
    
    const modal = new bootstrap.Modal(document.getElementById('paymentModal'));
    modal.show();
}

// Image Upload Functions
function previewImage(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('previewImg').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
            document.querySelector('.file-upload-area').style.display = 'none';
        }
        reader.readAsDataURL(file);
    }
}

function removeImage() {
    document.getElementById('image').value = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.querySelector('.file-upload-area').style.display = 'block';
}

// Drag and Drop Functionality
function initializeDragAndDrop() {
    const uploadArea = document.querySelector('.file-upload-area');
    const fileInput = document.getElementById('image');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                previewImage(fileInput);
            }
        });
    }
}

// Delete Confirmation Function
function confirmDelete(productId, productName) {
    document.getElementById('productName').textContent = productName;
    document.getElementById('confirmDelete').href = `/delete-product/${productId}`;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

// Confetti Effect for Success Page
function createConfetti() {
    const colors = ['#10b981', '#6366f1', '#8b5cf6', '#f59e0b', '#ef4444'];
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
        document.body.appendChild(confetti);
        
        // Remove confetti after animation
        setTimeout(() => {
            confetti.remove();
        }, 5000);
    }
}

// Initialize functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize drag and drop for file uploads
    initializeDragAndDrop();
    
    // Initialize confetti for success page
    if (document.querySelector('.success-container')) {
        createConfetti();
    }
}); 