document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JS Loaded!");

    const paymentMethod = document.getElementById("paymentMethod");
    const upiSection = document.getElementById("upiSection");
    const paymentForm = document.getElementById("paymentForm");

    if (!paymentForm) {
        console.error("⚠️ Payment form not found!");
        return;
    }

    // Show/hide fields based on payment method
    paymentMethod.addEventListener("change", function () {
        if (this.value === "UPI") {
            upiSection.style.display = "block";
        } else {
            upiSection.style.display = "none";
        }
    });

    // Form submission handler
    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault();
        console.log("✅ Submit button clicked!");

        const selectedMethod = paymentMethod.value;
        const csrfToken = document.getElementById("csrfToken").value;
        const amount = document.getElementById("amount").value;
        if (!selectedMethod) {
            alert("❌ Please select a valid payment method.");
            return;
        }

        if (!amount || amount <= 0) {
            alert("❌ Please enter a valid amount.");
            return;
        }
        
        let data = {
            amount: parseFloat(amount),
            type: selectedMethod === "UPI" ? 2 : 1, // Enum Mapping
            pay_status: 1, // Pending status
            created_by: parseInt(userId), // Ensure it's sent as an integer
        };
        console.log(data)

        if (selectedMethod === "UPI") {
            const upiId = document.getElementById("upiId").value;
            if (!upiId) {
                alert("❌ Please enter your UPI ID.");
                return;
            }
            data.upi_id = upiId;
        } 

        // Send data to Django backend
        fetch(`/payment/create/${bookingId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(responseData => {
            console.log("✅ Server Response:", responseData);
            if (responseData.payment_id) {
                window.location.href = `/payment/receipt/${responseData.payment_id}`;
            } else {
                alert("❌ Payment Failed: " + (responseData.error || "Unknown Error"));
            }
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert("❌ Payment request failed. Please try again.");
        });
    });
});

