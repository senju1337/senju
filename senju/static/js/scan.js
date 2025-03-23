// Get all needed elements
const dropzoneFile = document.getElementById("dropzone-file");
const uploadArea = document.getElementById("upload-area");
const imagePreview = document.getElementById("image-preview");
const previewImg = document.getElementById("preview-img");
const removeImageBtn = document.getElementById("remove-image");
const responseBox = document.getElementById("response-box");
const submitButton = document.getElementById("submit-button");
const errorMessage = document.getElementById("error-message");
const yesButton = document.getElementById("yes-button");
const noButton = document.getElementById("no-button");
const generatingHaikuBox = document.getElementById("generating-haiku-box");
const generatedHaikuBox = document.getElementById("generated-haiku-box");
let imageUploaded = false;

function handleFileSelect(event) {
  const file = event.target.files[0];

  if (file && file.type.startsWith("image/")) {
    // Create a URL for the selected image
    const imageUrl = URL.createObjectURL(file);

    // Set the image source
    previewImg.src = imageUrl;

    // Hide upload area and show image preview
    uploadArea.classList.add("hidden");
    imagePreview.classList.remove("hidden");
    errorMessage.classList.add("hidden");

    // Set flag that image is uploaded
    imageUploaded = true;
  }
}

function removeImage() {
  dropzoneFile.value = "";

  // Hide image
  imagePreview.classList.add("hidden");
  uploadArea.classList.remove("hidden");

  URL.revokeObjectURL(previewImg.src);
  previewImg.src = "";

  imageUploaded = false;
  responseBox.classList.add("opacity-0");
  generatingHaikuBox.classList.add("hidden");
  setTimeout(() => {
    document.getElementById("ai-response").textContent = "Waiting for input...";
  }, 500);
}

function handleSubmit() {
  if (imageUploaded) {
    // Hide error
    errorMessage.classList.add("hidden");

    // Show loading state
    document.getElementById("ai-response").textContent = "Analyzing image...";
    responseBox.classList.remove("opacity-0");

    // Get the file from the input
    const file = dropzoneFile.files[0];

    // Create FormData object to send the file
    const formData = new FormData();
    formData.append("image", file);

    // Send the image to your backend API
    fetch("/api/v1/image_reco", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Extract top result and display it
        if (data.results && data.results.length > 0) {
          const topResult = data.results[0];
          document.getElementById("ai-response").textContent =
            `${topResult.label} (${Math.round(topResult.confidence * 100)}% confidence)`;
        } else {
          document.getElementById("ai-response").textContent =
            "Could not identify the image";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("ai-response").textContent =
          "Error analyzing image";
      });
  } else {
    errorMessage.classList.remove("hidden");
    uploadArea.classList.add("shake");
    setTimeout(() => {
      uploadArea.classList.remove("shake");
    }, 600);
  }
}

function handleYesClick() {
  // Hide response box
  responseBox.classList.add("opacity-0");

  // Show generating haiku box first
  setTimeout(() => {
    responseBox.classList.add("hidden");
    generatingHaikuBox.classList.remove("hidden");

    // After a delay, hide generating box and show result
    setTimeout(() => {
      generatingHaikuBox.classList.add("hidden");
      generatedHaikuBox.classList.remove("hidden");
    }, 3000); // Show loading animation for 3 seconds before revealing the haiku
  }, 500); // Wait for response box fade out
}
function handleNoClick() {
  // Reset everything
  removeImage();
}

dropzoneFile.addEventListener("change", handleFileSelect);
removeImageBtn.addEventListener("click", removeImage);
submitButton.addEventListener("click", handleSubmit);
yesButton.addEventListener("click", handleYesClick);
noButton.addEventListener("click", handleNoClick);

// Add some CSS animation
document.head.insertAdjacentHTML(
  "beforeend",
  `
        <style>
            @keyframes shake {
                0% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                50% { transform: translateX(5px); }
                75% { transform: translateX(-5px); }
                100% { transform: translateX(0); }
            }
            .shake {
                animation: shake 0.5s ease-in-out;
                border-color: #ef4444 !important;
            }
        </style>
        `,
);
