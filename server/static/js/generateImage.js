function generateImage() {
    const deviceDropdown = document.getElementById('deviceDropdown');
    const selectedDevice = deviceDropdown.value;
    
    $("#loadingSpinner").show(); // Show the spinner

    $.ajax({
        url: `/api/take_photos_all`, // The correct API endpoint
        type: 'GET',
        success: function(photosData) {
            // Hide the spinner
            $("#loadingSpinner").hide();

            const imageDisplayArea = document.getElementById('imageDisplayArea');
            imageDisplayArea.innerHTML = ''; // Clear the area

            // Iterate over the array of photo data objects
            photosData.forEach(photoData => {
                // Check if there is an error key in the object
                if (photoData.error) {
                    console.error('Error for client:', photoData.client_id, photoData.error);
                    // Optionally, add an error message to the imageDisplayArea
                    const errorDiv = document.createElement('div');
                    errorDiv.textContent = `Error for client ${photoData.client_id}: ${photoData.error}`;
                    imageDisplayArea.appendChild(errorDiv);
                } else {
                    // Create an image element for the base64 image string
                    const img = document.createElement('img');
                    img.src = 'data:image/jpeg;base64,' + photoData.photo; // Set the src to the base64 string
                    img.style.maxWidth = '100%';
                    img.classList.add('col-md-4'); // Bootstrap class for a 3-column layout
                    imageDisplayArea.appendChild(img); // Add the image to the display area
                }
            });
        },
        error: function(error) {
            // Hide the spinner
            $("#loadingSpinner").hide();
            
            console.error('Error generating images:', error);
        }
    });
}