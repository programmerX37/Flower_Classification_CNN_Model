// Select elements
const inputImg = document.getElementById('InputImg');
const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const resultSection = document.getElementById('results');
const resultImage = document.getElementById('resultImage');
const predictionText = document.getElementById('predictionText');
const confidenceText = document.getElementById('confidenceText');
const uploadBar = document.getElementById('upload-bar');

// Listen for file selection on imageInput
imageInput.addEventListener('change', function () {
    console.log(document.getElementById('imageInput').files[0]);
    const file = this.files[0];
    if (file) {
        showImagePreview(file);
        uploadImage(file);
    }
});

// Listen for file selection on InputImg
inputImg.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        showImagePreview(file);
        uploadImage(file);
    }
});

// Optional: Add drag & drop support
uploadBar.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBar.classList.add('drag-over');
});

uploadBar.addEventListener('dragleave', () => {
    uploadBar.classList.remove('drag-over');
});

uploadBar.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBar.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) {
        showImagePreview(file);
        uploadImage(file);
    }
});

// Show image preview
function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Upload image to Flask backend
function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Update result UI
        resultSection.style.display = 'block';
        resultImage.src = previewImage.src;
        predictionText.textContent = `Prediction: ${data.flower}`;
        confidenceText.textContent = `Confidence: ${data.confidence}`;
    })
    .catch(err => {
        console.error('Upload failed:', err);
        alert('An error occurred while uploading.');
    });
}
