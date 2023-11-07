function takePhoto() {
    const deviceDropdown = document.getElementById("deviceDropdown");
    const deviceId = deviceDropdown.value;

    $("#loadingSpinner").show(); // Show the spinner

    fetch(`/api/take_photo/${deviceId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.blob(); // Convert the response data to a blob
        })
        .then(blob => {
            // Hide the spinner
            $("#loadingSpinner").hide();

            const url = window.URL.createObjectURL(blob);
            const image = document.getElementById("photoDisplay");
            image.src = url;
            image.onload = () => {
                window.URL.revokeObjectURL(url); // Revoke the Blob URL once the image is loaded
            };
            image.style.display = "block"; // Display the image
        })
        .catch(error => {
            // Hide the spinner
            $("#loadingSpinner").hide();
            
            console.error("Error taking photo:", error);
        });
}