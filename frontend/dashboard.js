fetch("https://i75nzp7qi7.execute-api.ap-south-1.amazonaws.com/attendance-records")

const table =
    document.getElementById("attendanceTable");

const API_URL =
    "https://i75nzp7qi7.execute-api.ap-south-1.amazonaws.com/attendance-records";

async function loadAttendance() {

    try {

        const response = await fetch(API_URL + "?t=" + new Date().getTime());

        if (!response.ok) {
            throw new Error("API Error");
        }

        const records = await response.json();

        table.innerHTML = "";

        let present = 0;
        let late = 0;
        let absent = 0;

        records.forEach(record => {

            const row = `
                <tr>
                    <td>${record.employee_id}</td>
                    <td>${record.date}</td>
                    <td>${record.clock_in || "-"}</td>
                    <td>${record.clock_out || "-"}</td>
                    <td>${record.status}</td>
                </tr>
            `;

            table.innerHTML += row;

            if (record.status === "present") present++;
            else if (record.status === "late") late++;
            else if (record.status === "absent") absent++;
        });

        document.getElementById("presentCount").innerText = present;
        document.getElementById("lateCount").innerText = late;
        document.getElementById("absentCount").innerText = absent;

    } catch (error) {
        console.error("Dashboard Load Error:", error);
    }
}

loadAttendance();