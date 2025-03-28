// Calendar //
document.addEventListener("DOMContentLoaded", function () {
    const monthYear = document.getElementById("monthYear");
    const calendarBody = document.getElementById("calendarBody");
    const prevMonth = document.getElementById("prevMonth");
    const nextMonth = document.getElementById("nextMonth");

    let currentDate = new Date();

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        
        const today = new Date();
        const todayDay = today.getDate();
        const todayMonth = today.getMonth();
        const todayYear = today.getFullYear();

        monthYear.textContent = `${date.toLocaleString("pt-BR", { month: "long" })} ${date.getFullYear()}`;

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        let html = "";
        let day = 1;

        for (let i = 0; i < 6; i++) {
            let row = "<tr>";
            for (let j = 0; j < 7; j++) {
                if ((i === 0 && j < firstDay) || day > lastDate) {
                    row += "<td></td>";
                } else {
                    let className = (day === todayDay && month === todayMonth && year === todayYear) ? "today" : "";
                    row += `<td class="${className}">${day}</td>`;
                    day++;
                }
            }
            row += "</tr>";
            html += row;
            if (day > lastDate) break;
        }

        calendarBody.innerHTML = html;
    }

    prevMonth.addEventListener("click", function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextMonth.addEventListener("click", function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    renderCalendar(currentDate);
});
