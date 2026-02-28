document.addEventListener("DOMContentLoaded", async function () {
    const tableBody = document.querySelector("#tasktable tbody");
    if (!tableBody) {
        console.error("Task table body not found");
        return;
    }

    const url = new URLSearchParams(window.location.search);
    const user_id = url.get("user_id");        


    try {
        const req = await fetch(`http://127.0.0.1:8000/getAllTasks/${user_id}`);
        if (!req.ok) {
            throw new Error("Failed to fetch tasks");
        }

        const response = await req.json();

        response.forEach((task) => {
            const row = `
                <tr data-id="${task.id}">
                    <td>${task.id ?? ""}</td>
                    <td>${task.name ?? ""}</td>
                    <td>${task.description ?? ""}</td>
                    <td>${task.duration ?? ""}</td>
                    <td>${task.priority ?? ""}</td>
                    <td class="status">${task.status ?? ""}</td>
                    <td class="actions-cell">
                    <button class="Mark As Complteted" id="edit button" onclick="markTaskCompleted(${task.id})">Mark as completed</button>
                    <button class="delete" onclick="deleteTask(${task.id})">Delete</button>
                     </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error(error);
        tableBody.innerHTML = '<tr><td colspan="6">Unable to load tasks</td></tr>';
    }
});

async function markTaskCompleted(taskId) {
    try{

        const resp = await fetch(`http://127.0.0.1:8000/markTaskCompleted/${taskId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!resp.ok) {
            throw new Error("updation failed")
        }

        const row=document.querySelector(`tr[data-id="${taskId}"]`);
        if (row){
            const statuscell=row.querySelector(".status");
            statuscell.textContent="COMPLETED"

        }
    }
    catch (error){
        console.log("failed to update task :",error);
    }
}

async function deleteTask(taskId) {
    try{

        const resp = await fetch(`http://127.0.0.1:8000/deleteTask/${taskId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!resp.ok) {
            throw new Error("Deletion failed");
        }
        const row=document.querySelector(`tr[data-id="${taskId}"]`);
        if(row) row.remove();
    }
    catch (error){
        console.error("failed to delete task")
    }
}

document.addEventListener("submit", async function (event) {
    if (event.target.id === "addTaskForm") {
        event.preventDefault();
        const url = new URLSearchParams(window.location.search);
        const user_id = url.get("user_id");        
        const formData = new FormData(event.target);
        const taskData = {
            name: formData.get("name"),
            description: formData.get("description"),
            duration: formData.get("duration"),
            priority: formData.get("priority")
        };

        try {
            const resp = await fetch(`http://127.0.0.1:8000/createTask/${user_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(taskData)
            });
            if (!resp.ok) {
                throw new Error("Failed to add task");
            }

            const newTask = await resp.json();

            const tableBody = document.querySelector("#tasktable tbody");

            const newRow = `
                <tr data-id="${newTask.id}">
                    <td>${newTask.id ?? ""}</td>
                    <td>${newTask.name ?? ""}</td>
                    <td>${newTask.description ?? ""}</td>
                    <td>${newTask.duration ?? ""}</td>
                    <td>${newTask.priority ?? ""}</td>
                    <td class="status">${newTask.status ?? ""}</td>
                    <td class="actions-cell">
                        <button onclick="markTaskCompleted(${newTask.id})">Mark as completed</button>
                        <button onclick="deleteTask(${newTask.id})">Delete</button>
                    </td>
                </tr>
                `;

            tableBody.insertAdjacentHTML("afterbegin", newRow);

            // Clear the form
            event.target.reset();
                    } catch (error) {
                        console.error("Error adding task:", error);
                    }
                }
});