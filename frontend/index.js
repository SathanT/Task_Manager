document.addEventListener("DOMContentLoaded", function () {
    // Fixed: match HTML id "userform" (was "userForm")
    const userForm = document.getElementById("userform");
    if (!userForm) {
        console.error("Form element #userform not found");
        return;
    }

    userForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const data = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value
        };

        try {
            // Fixed: use explicit backend URL so frontend works even when not served by FastAPI
            const response = await fetch("http://127.0.0.1:8000/createUser", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Fixed: handle backend errors instead of rendering invalid output
            if (!response.ok) {
                throw new Error(result.detail || "User creation failed");
            }

            renderTable(result);
        } catch (error) {
            alert(error.message);
            console.error(error);
        }
    });
});

function renderTable(data) {
    // Fixed: match HTML id "formsection" (was "formSection")
    document.getElementById("formsection").classList.add("hidden");
    document.getElementById("SuccessSection").classList.remove("hidden");

    const container = document.getElementById("responseContainer");
    container.innerHTML = `
        <p><strong>User Id:</strong> ${data.id}</p>
        <p><strong>User Name:</strong> ${data.name}</p>
        <p><strong>Email:</strong> ${data.email}</p>
    `;
}