    fetch('/api/check-login/')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                document.getElementById('profile-link').innerHTML = `
                    <img src="${data.profile_photo_url}" alt="Profile" style="width:40px; height:40px; border-radius:50%;">
                `;
            }
        })
        .catch(error => console.error('Error checking login status:', error));

  






document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/check-login/')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                let profileLink = document.getElementById('profile-link');
                profileLink.innerHTML = `
                    <img id="profile-img" src="${data.profile_photo_url}" alt="Profile" 
                        style="width:40px; height:40px; border-radius:50%; cursor:pointer;">
                `;

                // Show dropdown on click
                document.getElementById("profile-img").addEventListener("click", function (event) {
                    event.preventDefault(); // Prevent navigation
                    let dropdown = document.getElementById("profile-dropdown");
                    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
                });

                // Hide dropdown when clicking outside
                document.addEventListener("click", function (event) {
                    let dropdown = document.getElementById("profile-dropdown");
                    let profileImg = document.getElementById("profile-img");

                    if (event.target !== dropdown && event.target !== profileImg) {
                        dropdown.style.display = "none";
                    }
                });
            }
        })
        .catch(error => console.error('Error checking login status:', error));
});

