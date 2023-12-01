function uploadFile() {
        var fileInput = document.getElementById('fileInput');
        var selectedFile = fileInput.files[0];
        console.log('Selected File:', selectedFile);

        // You can implement the backend logic to handle the file here
        // For now, this function simply logs the selected file to the console
    }