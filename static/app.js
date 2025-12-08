async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();
    const list = document.getElementById("taskList");
    
    if (tasks.length === 0) {
        list.innerHTML = '<div class="empty-state"><p>🎯 No tasks yet. Add one to get started!</p></div>';
        return;
    }
    
    list.innerHTML = "";
    tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = `task-item ${task.completed ? 'completed' : ''}`;

        li.innerHTML = `
            <div class="task-actions">
                <input 
                    type="checkbox" 
                    class="task-checkbox"
                    ${task.completed ? "checked" : ""} 
                    onchange="toggleTask(${task.id}, this.checked)"
                >
                <span class="task-text">${task.title}</span>
            </div>
            <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
        `;

        list.appendChild(li);
    });
}

async function addTask() {
    const title = document.getElementById("taskInput").value.trim();
    if (!title) {
        alert("Please enter a task!");
        return;
    }

    try {
        const res = await fetch("/api/tasks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title})
        });

        if (res.ok) {
            document.getElementById("taskInput").value = "";
            loadTasks();
        } else {
            alert("Failed to add task");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error adding task");
    }
}

async function toggleTask(id, completed) {
    try {
        await fetch(`/api/tasks/${id}`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({completed})
        });
        loadTasks();
    } catch (error) {
        console.error("Error:", error);
    }
}

async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }
    
    try {
        const res = await fetch(`/api/tasks/${id}`, {method: "DELETE"});
        if (res.ok) {
            loadTasks();
        } else {
            alert("Failed to delete task");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error deleting task");
    }
}

// Load tasks on page load
loadTasks();
