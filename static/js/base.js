document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/check-login/')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                let profileLink = document.getElementById('profile-link');
                profileLink.innerHTML = `
                    <img id="profile-img" src="${data.profile_photo_url}" alt="Profile style="dislay:block;" 
                        style="width:40px; height:40px; border-radius:50%; cursor:pointer;margin-left: 18px;">
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



// Highlight the active navbar link based on the current URL path

document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL path
    let currentPath = window.location.pathname;

    // Select all navbar links
    let navLinks = document.querySelectorAll("#navber li a");

    // Loop through each link
    navLinks.forEach(link => {
        // Check if the link's href matches the current path
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active"); // Add active class
        } else {
            link.classList.remove("active"); // Remove from others
        }
    });
});



function open_slidebar(){
    let profileLink = document.getElementById('profile-link');
    profileLink.style.display="none";
}
function undo(){
    let profileLink = document.getElementById('profile-link');
    profileLink.style.display="block";
}
