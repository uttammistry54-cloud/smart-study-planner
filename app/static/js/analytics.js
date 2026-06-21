document.addEventListener("DOMContentLoaded", () => {
    const PRIMARY = "#4F3FF0";
    const ACCENT = "#F5A524";
    const SUCCESS = "#1FAA59";
    const DANGER = "#E5484D";
    const PALETTE = ["#4F3FF0", "#F5A524", "#1FAA59", "#6B8AFD", "#E5484D", "#9A96BE", "#3D2FCC"];

    // ---------- Weekly Study Hours (Bar Chart) ----------
    fetch("/analytics/api/weekly-hours")
        .then((res) => res.json())
        .then((data) => {
            const ctx = document.getElementById("weeklyHoursChart");
            if (!ctx) return;
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: "Hours Studied",
                            data: data.hours,
                            backgroundColor: PRIMARY,
                            borderRadius: 6,
                            maxBarThickness: 40,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: "#E7E5F0" } },
                        x: { grid: { display: false } },
                    },
                },
            });
        })
        .catch((err) => console.error("Failed to load weekly hours:", err));

    // ---------- Task Completion Rate (Doughnut Chart) ----------
    fetch("/analytics/api/completion-rate")
        .then((res) => res.json())
        .then((data) => {
            const ctx = document.getElementById("completionRateChart");
            const statsEl = document.getElementById("completionStats");
            if (!ctx) return;

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["Completed", "Pending"],
                    datasets: [
                        {
                            data: [data.completed, data.pending],
                            backgroundColor: [SUCCESS, "#E7E5F0"],
                            borderWidth: 0,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "70%",
                    plugins: { legend: { position: "bottom" } },
                },
            });

            if (statsEl) {
                statsEl.textContent = `${data.completion_rate}% complete — ${data.completed} of ${data.total} tasks done`;
            }
        })
        .catch((err) => console.error("Failed to load completion rate:", err));

    // ---------- Time by Subject (Pie Chart) ----------
    fetch("/analytics/api/subject-breakdown")
        .then((res) => res.json())
        .then((data) => {
            const ctx = document.getElementById("subjectBreakdownChart");
            if (!ctx) return;

            if (!data.labels.length) {
                ctx.parentElement.innerHTML =
                    '<p class="empty-state">No study sessions logged yet. Log time from the Dashboard to see this chart.</p>';
                return;
            }

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            data: data.minutes,
                            backgroundColor: PALETTE,
                            borderWidth: 0,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        })
        .catch((err) => console.error("Failed to load subject breakdown:", err));

    // ---------- Weekly Task Completion Progress (Line Chart) ----------
    fetch("/analytics/api/weekly-progress")
        .then((res) => res.json())
        .then((data) => {
            const ctx = document.getElementById("weeklyProgressChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: "Tasks Completed",
                            data: data.completed_counts,
                            borderColor: ACCENT,
                            backgroundColor: "rgba(245, 165, 36, 0.15)",
                            fill: true,
                            tension: 0.35,
                            pointBackgroundColor: ACCENT,
                            pointRadius: 4,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: "#E7E5F0" } },
                        x: { grid: { display: false } },
                    },
                },
            });
        })
        .catch((err) => console.error("Failed to load weekly progress:", err));
});
