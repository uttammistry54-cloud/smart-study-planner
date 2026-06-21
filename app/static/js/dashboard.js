// ============================================
// Mobile Sidebar Toggle (used on every page)
// ============================================
document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");

    if (menuToggle && sidebar && overlay) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.add("open");
            overlay.classList.add("show");
        });
        overlay.addEventListener("click", () => {
            sidebar.classList.remove("open");
            overlay.classList.remove("show");
        });
    }

    // ============================================
    // Dashboard: Add Goal toggle + save
    // ============================================
    const addGoalBtn = document.getElementById("addGoalBtn");
    const addGoalForm = document.getElementById("addGoalForm");
    const saveGoalBtn = document.getElementById("saveGoalBtn");

    if (addGoalBtn && addGoalForm) {
        addGoalBtn.addEventListener("click", () => {
            addGoalForm.classList.toggle("hidden");
        });
    }

    if (saveGoalBtn) {
        saveGoalBtn.addEventListener("click", async () => {
            const subjectInput = document.getElementById("goalSubject");
            const minutesInput = document.getElementById("goalMinutes");
            const subject = subjectInput.value.trim() || "Overall";
            const targetMinutes = parseInt(minutesInput.value, 10);

            if (!targetMinutes || targetMinutes <= 0) {
                alert("Please enter a valid number of minutes.");
                return;
            }

            try {
                const res = await fetch("/dashboard/goals", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ subject, target_minutes: targetMinutes }),
                });
                if (res.ok) {
                    window.location.reload();
                } else {
                    const data = await res.json();
                    alert(data.error || "Could not save goal.");
                }
            } catch (err) {
                alert("Network error. Please try again.");
            }
        });
    }

    // ============================================
    // Dashboard: Quick Log Study Session
    // ============================================
    const logSessionBtn = document.getElementById("logSessionBtn");

    if (logSessionBtn) {
        logSessionBtn.addEventListener("click", async () => {
            const subjectInput = document.getElementById("logSubject");
            const minutesInput = document.getElementById("logMinutes");
            const subject = subjectInput.value.trim();
            const durationMin = parseInt(minutesInput.value, 10);

            if (!subject) {
                alert("Please enter a subject.");
                return;
            }
            if (!durationMin || durationMin <= 0) {
                alert("Please enter a valid number of minutes.");
                return;
            }

            try {
                const res = await fetch("/dashboard/log-session", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ subject, duration_min: durationMin }),
                });
                if (res.ok) {
                    window.location.reload();
                } else {
                    const data = await res.json();
                    alert(data.error || "Could not log session.");
                }
            } catch (err) {
                alert("Network error. Please try again.");
            }
        });
    }
});
