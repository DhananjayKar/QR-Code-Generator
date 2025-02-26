document.addEventListener('DOMContentLoaded', function () {
    document.documentElement.lang = "en";

    const form = document.getElementById('qrForm');
    const textInput = document.getElementById('textInput');
    const fileInput = document.getElementById('fileInput');
    const fileDisplay = document.getElementById('fileDisplay');
    const removeFile = document.getElementById('removeFile');
    const qrImage = document.getElementById('qrImage');

    // Handle file selection
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            fileDisplay.textContent = fileInput.files[0].name;
            fileDisplay.classList.remove('d-none');
            removeFile.classList.remove('d-none');
        }
    });

    // Remove file selection
    removeFile.addEventListener('click', function () {
        fileInput.value = "";
        fileDisplay.textContent = "";
        fileDisplay.classList.add('d-none');
        removeFile.classList.add('d-none');
    });

    // Handle form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        let formData = new FormData(form);
        for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }
        if (!textInput.value.trim() && fileInput.files.length === 0) {
            alert('Please enter text or upload a file.');
            return;
        }

        fetch('/generate_qr', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to generate QR code');
            return response.blob();
        })
        .then(blob => {
            if (qrImage.src) URL.revokeObjectURL(qrImage.src); // Free memory from previous QR codes
            qrImage.src = URL.createObjectURL(blob);
            qrImage.classList.remove('d-none');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating QR code. Please try again.');
            qrImage.classList.add('d-none');
        });
    });
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
});