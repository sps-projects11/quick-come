
$(document).ready(function() {
    $.ajax({
        url: "{% url 'user-profile' %}",  // Replace with your URL name
        type: "GET",
        dataType: "json",
        success: function(response) {
            $("#profile-pic").attr("src", response.photo);
            $("#profile-name").text(response.fullname);
            $("#profile-info").text("User Profile Loaded");
        },
        error: function() {
            $("#profile-info").text("Failed to load user data");
        }
    });
});
