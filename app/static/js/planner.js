document.addEventListener("DOMContentLoaded", () => {
    const addSlotModal = document.getElementById("addSlotModal");
    const addExamModal = document.getElementById("addExamModal");
    const openAddSlotBtn = document.getElementById("openAddSlotBtn");
    const openAddExamBtn = document.getElementById("openAddExamBtn");

    if (openAddSlotBtn && addSlotModal) {
        openAddSlotBtn.addEventListener("click", () => {
            addSlotModal.classList.remove("hidden");
        });
    }

    if (openAddExamBtn && addExamModal) {
        openAddExamBtn.addEventListener("click", () => {
            addExamModal.classList.remove("hidden");
        });
    }

    document.querySelectorAll(".modal-close").forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-close");
            const target = document.getElementById(targetId);
            if (target) target.classList.add("hidden");
        });
    });

    document.querySelectorAll(".modal-overlay").forEach((overlay) => {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                overlay.classList.add("hidden");
            }
        });
    });
});
