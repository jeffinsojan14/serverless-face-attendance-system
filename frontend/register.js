const registerBtn =
    document.getElementById("registerBtn");

const statusText =
    document.getElementById("status");

registerBtn.addEventListener("click", async () => {

    const employeeId =
        document.getElementById("employeeId").value;

    const employeeName =
        document.getElementById("employeeName").value;

    const imageFile =
        document.getElementById("employeeImage").files[0];

    if (!employeeId || !employeeName || !imageFile) {

        alert("Fill all fields");

        return;
    }

    try {

        statusText.innerText =
            "Requesting upload URL...";

        const response = await fetch(
            "https://i75nzp7qi7.execute-api.ap-south-1.amazonaws.com/generate-registration-upload-url"
);

        const data = await response.json();

        const parsed =
            data.body ? JSON.parse(data.body) : data;

        statusText.innerText =
            "Uploading employee image...";

        await fetch(parsed.uploadURL, {

            method: "PUT",

            headers: {
                "Content-Type": imageFile.type
            },

            body: imageFile
        });

        statusText.innerText =
            "Employee registered successfully";

    } catch (error) {

        console.error(error);

        statusText.innerText =
            "Registration failed";
    }

});