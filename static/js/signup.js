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

    function showToast(message, type = "success") {
        showToastMessage(message, type); // Using toaster for notifications
    }

    async function sendOTP() {
        const email = document.getElementById("email").value.trim();
        if (!email) {
            showToast("Please enter your email.", "error");
            return;
        }

        try {
            const response = await fetch(`/request-otp/?email=${encodeURIComponent(email)}`);
            const data = await response.json();
            showToast(data.message || "OTP sent successfully.");
        } catch (error) {
            console.error("Error:", error);
            showToast("Failed to send OTP. Please try again.", "error");
        }
    }

    async function verifyOTP() {
        const email = document.getElementById("email").value.trim();
        const otp = document.getElementById("otp").value.trim();
        const firstName = document.getElementById("first_name").value.trim();
        const lastName = document.getElementById("last_name").value.trim();
        const dob = document.getElementById("dob").value.trim();

        if (!email || !otp || !dob) {
            showToast("Please fill in all required fields.", "error");
            return;
        }

        const formData = new FormData();
        formData.append("email", email);
        formData.append("otp", otp);
        formData.append("first_name", firstName);
        formData.append("last_name", lastName);
        formData.append("dob", dob);

        try {
            const response = await fetch("/verify-otp/", {
                method: "POST",
                headers: { "X-CSRFToken": 'csrfToken' },
                body: formData,
            });

            const data = await response.json();
            showToast(data.message, data.status === "success" ? "success" : "error");
        } catch (error) {
            console.error("Error:", error);
            showToast("Failed to verify OTP. Please try again.", "error");
        }
    }

    async function submitSignup(event) {
        event.preventDefault(); // Prevent default form submission
        const formData = new FormData(signupForm);

        try {
            const response = await fetch("/sign-up/", {
                method: "POST",
                headers: { "X-CSRFToken": 'csrfToken'},
                body: formData,
            });

            const data = await response.json();
            showToast(data.message, data.status === "success" ? "success" : "error");

            if (data.status === "success") {
                window.location.href = data.redirect;
            }
        } catch (error) {
            console.error("Error:", error);
            showToast("Signup failed. Please try again.", "error");
        }
    }

    sendOtpButton.addEventListener("click", sendOTP);
    verifyOtpButton.addEventListener("click", verifyOTP);
    signupForm.addEventListener("submit", submitSignup);
});
