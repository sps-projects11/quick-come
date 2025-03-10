
document.getElementById("signin-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent normal form submission
    
    let formData = new FormData(this);

    fetch("{% url 'sign_in' %}", {  // Send request to sign-in view
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
