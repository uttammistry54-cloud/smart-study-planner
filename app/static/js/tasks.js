document.addEventListener("DOMContentLoaded", () => {
    const addTaskModal = document.getElementById("addTaskModal");
    const editTaskModal = document.getElementById("editTaskModal");
    const openAddTaskBtn = document.getElementById("openAddTaskBtn");
    const editTaskForm = document.getElementById("editTaskForm");

    // Open Add Task modal
    if (openAddTaskBtn && addTaskModal) {
        openAddTaskBtn.addEventListener("click", () => {
            addTaskModal.classList.remove("hidden");
        });
    }

    // Close modal buttons (data-close attribute holds target modal id)
    document.querySelectorAll(".modal-close").forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-close");
            const target = document.getElementById(targetId);
            if (target) target.classList.add("hidden");
        });
    });

    // Close modal when clicking outside the modal box
    document.querySelectorAll(".modal-overlay").forEach((overlay) => {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                overlay.classList.add("hidden");
            }
        });
    });

    // Open Edit Task modal, pre-fill fields, set form action
    document.querySelectorAll(".edit-task-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-id");
            const title = btn.getAttribute("data-title");
            const subject = btn.getAttribute("data-subject");
            const description = btn.getAttribute("data-description");
            const dueDate = btn.getAttribute("data-due-date");
            const priority = btn.getAttribute("data-priority");

            document.getElementById("edit_title").value = title;
            document.getElementById("edit_subject").value = subject;
            document.getElementById("edit_description").value = description;
            document.getElementById("edit_due_date").value = dueDate;
            document.getElementById("edit_priority").value = priority;

            editTaskForm.action = `/tasks/edit/${id}`;
            editTaskModal.classList.remove("hidden");
        });
    });
});
