document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/check-login/')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                let profileLinks = document.querySelectorAll('#profile-link'); // Select all profile-link elements
                
                profileLinks.forEach(profileLink => {
                    profileLink.innerHTML = `
                        <img class="profile-img" src="${data.profile_photo_url}" 
                            alt="Profile" style="width:40px; height:40px; border-radius:50%; cursor:pointer;margin-left: 18px;">
                    `;
                });

                // Show dropdown on click
                document.querySelectorAll(".profile-img").forEach(img => {
                    img.addEventListener("click", function (event) {
                        event.preventDefault(); // Prevent navigation
                        let dropdown = this.closest("div").querySelector("#profile-dropdown");
                        dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
                    });
                });

                // Hide dropdown when clicking outside
                document.addEventListener("click", function (event) {
                    let dropdowns = document.querySelectorAll("#profile-dropdown");
                    let profileImgs = document.querySelectorAll(".profile-img");

                    dropdowns.forEach(dropdown => {
                        if (![...profileImgs].includes(event.target) && event.target !== dropdown) {
                            dropdown.style.display = "none";
                        }
                    });
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



function open_slidebar() {
    document.querySelectorAll('#profile-link').forEach(link => {
        link.style.display = "none";
    });
}

function undo() {
    document.querySelectorAll('#profile-link').forEach(link => {
        link.style.display = "block";
    });
}

