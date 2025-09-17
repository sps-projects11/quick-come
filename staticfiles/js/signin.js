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
            "X-CSRFToken": 'csrftoken'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            setTimeout(() => {
                // Redirect to home page or wherever specified
                window.location.href = data.redirect; 

            },2000);
        } 
        loader.style.display = "none";  // Hide loading spinner
    })
    .catch(error => {
        loader.style.display = "none";  // Hide loading spinner
        console.error("Error during login:", error);
    });
}