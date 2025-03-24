// profileUploader.js
export function initProfileUploader(config) {
    const {
      profileContainerSelector,
      fileInputId,
      profilePreviewId,
      removePhotoIconId,
      plusIconSelector,
      defaultImage = '/static/all-Pictures/Feature boxes/location.jpg'
    } = config;
  
    const profileContainer = document.querySelector(profileContainerSelector);
    const fileInput = document.getElementById(fileInputId);
    const profilePreview = document.getElementById(profilePreviewId);
    const removePhotoIcon = document.getElementById(removePhotoIconId);
    const plusIcon = document.querySelector(plusIconSelector);
  
    // Clicking the plus icon opens the file dialog
    plusIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });
  
    // When file is selected, update preview and add "has-image" class
    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          profilePreview.src = e.target.result;
          profileContainer.classList.add('has-image');
        };
        reader.readAsDataURL(file);
      }
    });
  
    // Clicking the remove icon clears the file and resets the image
    removePhotoIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.value = "";
      profilePreview.src = defaultImage;
      profileContainer.classList.remove('has-image');
    });
  }
  