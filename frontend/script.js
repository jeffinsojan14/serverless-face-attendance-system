const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("captureBtn");
const uploadBtn = document.getElementById("uploadBtn");
const previewImage = document.getElementById("previewImage");
const statusText = document.getElementById("status");

let capturedBlob = null;

/* ---------------- START CAMERA ---------------- */
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;
    } catch (error) {
        console.error(error);
        alert("Camera access denied or not available");
    }
}

startCamera();

/* ---------------- CAPTURE IMAGE ---------------- */
captureBtn.addEventListener("click", () => {

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {

        if (!blob) {
            alert("Capture failed");
            return;
        }

        capturedBlob = blob;

        previewImage.src = URL.createObjectURL(blob);

        statusText.innerText = "Face captured successfully";

    }, "image/jpeg", 0.95);
});

/* ---------------- UPLOAD TO AWS ---------------- */
uploadBtn.addEventListener("click", async () => {

    if (!capturedBlob) {
        alert("Please capture image first");
        return;
    }

    try {
        statusText.innerText = "Requesting upload URL...";

        const response = await fetch(
            "https://i75nzp7qi7.execute-api.ap-south-1.amazonaws.com/generate-upload-url"
        );

        const data = await response.json();

        // SAFE PARSING (handles Lambda response format)
        const parsed = data.body ? JSON.parse(data.body) : data;

        const uploadURL = parsed.uploadURL;

        statusText.innerText = "Uploading image...";

        const uploadResponse = await fetch(uploadURL, {
            method: "PUT",
            headers: {
                "Content-Type": "image/jpeg"
            },
            body: capturedBlob
        });

        if (!uploadResponse.ok) {
            throw new Error("S3 upload failed");
        }

        statusText.innerText = "Upload successful 🎉";

    } catch (error) {
        console.error(error);
        statusText.innerText = "Upload failed ❌ Check console";
    }
});