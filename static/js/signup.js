let currentIndex = 0;
const slides = document.querySelectorAll(".carousel img");
const totalSlides = slides.length;
const carousel = document.querySelector(".carousel");

function updateSlide() {
    const offset = -currentIndex * 100;
    carousel.style.transform = `translateX(${offset}%)`;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateSlide();
}

setInterval(nextSlide, 5000);




document.addEventListener("DOMContentLoaded", function () {
    let sendOtpButton = document.getElementById("sendOtp");
    let verifyOtpButton = document.getElementById("verifyOtp");
    let signupForm = document.getElementById("signupForm");

    // Send OTP
    sendOtpButton.addEventListener("click", function () {
        let email = document.getElementById("email").value;

        if (!email) {
            alert("Please enter your email address.");
            return;
        }

        fetch(`/request-otp/?email=${encodeURIComponent(email)}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)

            })
            .catch(error => console.error("Error:", error));
    });

    // Verify OTP
    verifyOtpButton.addEventListener("click", function () {
        let email = document.getElementById("email").value;
        let otp = document.getElementById("otp").value;
        let firstName = document.getElementById("first_name").value;
        let lastName = document.getElementById("last_name").value;
        let dob = document.getElementById("dob").value;
        let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        if (!email || !otp || !dob) {
            alert("Email, OTP, and DOB are required.");
            return;
        }

        let formData = new FormData();
        formData.append("email", email);
        formData.append("otp", otp);
        formData.append("first_name", firstName);
        formData.append("last_name", lastName);
        formData.append("dob", dob);

        fetch("/verify-otp/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.status === "success") {
                console.log("OTP verified successfully.");
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Submit Signup Form
    signupForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(signupForm);

        fetch("/sign-up/", {
            method: "POST",
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect; // Redirect to sign-in page
            } 
            })
        .catch(error => console.error("Error:", error));
    });
});
