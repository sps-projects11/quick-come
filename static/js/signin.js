document.getElementById("signin-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent normal form submission

    let formData = new FormData(this);
    let signInUrl = this.action; // Get the form's action URL

    fetch(signInUrl, {  // Use the correct URL from the form
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            window.location.href = data.redirect;  // Redirect to home page
        }
    })
    .catch(error => console.error("Error:", error));
});

