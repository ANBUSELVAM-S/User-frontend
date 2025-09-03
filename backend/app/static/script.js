const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const result = document.getElementById("result");
const labelEl = document.getElementById("label");
const preview = document.getElementById("preview");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.src = e.target.result;
    preview.innerHTML = "";
    preview.appendChild(img);
  };
  reader.readAsDataURL(file);
});

uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) { 
    alert("Please choose an image first."); 
    return; 
  }

  const formData = new FormData();
  formData.append("file", file);

  uploadBtn.disabled = true;
  uploadBtn.textContent = "Predicting...";

  try {
    const resp = await fetch("/predict", {
      method: "POST",
      body: formData
    });
    if (!resp.ok) {
      throw new Error("Server error");
    }
    const data = await resp.json();

    // ✅ Only show label
    labelEl.textContent = data.label;

    result.hidden = false;
  } catch (e) {
    alert("Prediction failed: " + e.message);
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Predict";
  }
});
