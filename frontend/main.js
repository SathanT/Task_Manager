async function validateUser() {
    const id = document.getElementById("user_id").value;
    const email = document.getElementById("email").value;

    document.getElementById("id_error").innerText = "";
    document.getElementById("email_error").innerText = "";

    const data = {
        id: Number(id),
        email: email
    };

    try {
        const req = await fetch("http://127.0.0.1:8000/validateUser", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (req.status === 404) {
            document.getElementById("id_error").innerText = "User not found";
            document.getElementById("email_error").innerText = "User not found";
            return;
        }

        if (!req.ok) {
            document.getElementById("email_error").innerText = "Unable to validate user";
            return;
        }
 
        const userId = document.getElementById("user_id").value;
        window.location.href = `user.html?user_id=${userId}`;
    } catch (error) {
        document.getElementById("email_error").innerText = "Backend is not reachable";
        console.error(error);
    }
}
