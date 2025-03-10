document.addEventListener("DOMContentLoaded", function () {
    // Handle payment method selection
    document.getElementById('paymentMethod').addEventListener('change', function() {
        const upiSection = document.getElementById('upiSection');
        const netBankingSection = document.getElementById('netBankingSection');

        if (this.value === 'UPI') {
            upiSection.style.display = 'block';
            netBankingSection.style.display = 'none';
        } else if (this.value === 'NetBanking') {
            upiSection.style.display = 'none';
            netBankingSection.style.display = 'block';
        } else { // Cash On Delivery
            upiSection.style.display = 'none';
            netBankingSection.style.display = 'none';
        }
    });

    // Handle form submission
    document.getElementById('paymentForm').addEventListener('submit', function(event) {
        event.preventDefault();

        let BookingId = 123;  // Replace with actual booking ID dynamically
        const amount = document.getElementById('amount').value;
        const method = document.getElementById('paymentMethod').value;
        const csrfToken = document.getElementById('csrfToken').value;

        // Collect form data based on payment method
        let data = {
            amount: parseFloat(amount),
            type: method === 'UPI' ? 3 : method === 'NetBanking' ? 2 : 1,  // Enum Mapping
            pay_status: 1,  // Assuming 'Pending'
            created_by: 1,  // Replace with actual user ID
        };

        if (method === 'UPI') {
            data.upi_id = document.getElementById('upiId').value;
        } else if (method === 'NetBanking') {
            data.bank_name = document.getElementById('bankName').value;
            data.bank_ac = document.getElementById('accountNumber').value;
            data.ifsc_code = document.getElementById('ifscCode').value;
        }

        // Make API request
        fetch(`/payment/create/${BookingId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(responseData => {
            console.log("Server Response:", responseData);
            if (responseData.payment_id) {
                alert('Payment Initiated! Transaction ID: ' + responseData.payment_id);
            } else {
                alert('Payment Failed: ' + (responseData.error || "Unknown Error"));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Payment request failed.');
        });
    });
});
