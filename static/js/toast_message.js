(function() {
  // Store the original fetch
  const originalFetch = window.fetch;
  
  // Override window.fetch
  window.fetch = function(...args) {
    return originalFetch(...args).then(response => {
      // Clone the response so we can read its JSON without affecting the original
      const clonedResponse = response.clone();
      clonedResponse.json().then(data => {
        // Check if the response JSON contains a message and a status
        if (data && (data.success || data.error) && data.message) {
          let icon = "info";
          if (data.success) {
            icon = "success";
          } else if (data.error) {
            icon = "error";
          }
          // Show toast for the AJAX response
          Swal.fire({
            icon: icon,
            title: data.message,
            timer: 3000,
            timerProgressBar: true,
            showConfirmButton: false
          });
        }
      }).catch((error) => {
        // If response is not JSON, do nothing.
      });
      
      return response;
    });
  };

  // Also, on DOMContentLoaded, show any Django messages from full page loads:
  document.addEventListener('DOMContentLoaded', function() {
    if (window.djangoMessages && Array.isArray(window.djangoMessages)) {
      window.djangoMessages.forEach(function(msg) {
        let icon = "info";
        if (msg.tags.indexOf("success") !== -1) {
          icon = "success";
        } else if (msg.tags.indexOf("error") !== -1) {
          icon = "error";
        } else if (msg.tags.indexOf("warning") !== -1) {
          icon = "warning";
        }
        Swal.fire({
          icon: icon,
          title: msg.message,
          timer: 3000,
          timerProgressBar: true,
          showConfirmButton: false
        });
      });
    }
  });
})();
