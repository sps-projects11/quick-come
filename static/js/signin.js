function login(event) {
    event.preventDefault();  // Prevent form submission

    let formData = new FormData(event.target);  // Get form data from the form
    let loader = document.getElementById("modal");
    console.log("print");
    loader.style.display = "block";  // Show loading spinner

    const url = '/sign-in/'  // Direct URL to which data will be sent

    fetch(url, {  // Send data to the correct URL
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            setTimeout(() => {
                // Redirect to home page or wherever specified
                window.location.href = data.redirect; 
            }, 3000);
        } else {
            // Show error message if login fails
            Swal.fire({
                icon: 'error',
                title: 'Login failed',
                text: data.message || 'Something went wrong. Please try again.'
            });
        }
    })
    .catch(error => {
        loader.style.display = "none";  // Hide loading spinner
        console.error("Error during login:", error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'An unexpected error occurred. Please try again later.'
        });
    });
}