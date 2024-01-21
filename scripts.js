// Get location and dimensions of a cell in the calendar table
function getCellLocation(row, col) {
    let table = document.getElementById("calendar");
    let cell = table.rows[row].cells[col];
    let rect = cell.getBoundingClientRect();
    // Getting scroll offsets
    var scrollLeft = document.documentElement.scrollLeft;
    var scrollTop = document.documentElement.scrollTop;
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft, width: rect.width, height: rect.height };
}

// Draw a box over cells depending on the bay, the time and vehicle type 
function drawBoxOverCells(row, time, vehicleType) {
    let cell = getCellLocation(row, time.getHours() - 6);
    console.log(cell);
    // offset based on the minutes of when the appointment is
    let xOffset = cell.width - time.getMinutes() * 100 / cell.width;
    let actualWidth = 0;
    // Getting the amount of time a vehicle needs to be serviced for
    // Cell.width corresponds to 1 hour
    if (vehicleType === "compact" || vehicleType === "medium" || vehicleType === "full-size") {
        actualWidth = 0.5 * cell.width;
    }
    else if (vehicleType === "class 1 truck") {
        actualWidth = cell.width;
    }
    else {
        actualWidth = 2 * cell.width;
    }
    // Creating the box
    var box = document.createElement("div");
    box.style.position = "absolute";
    box.style.top = cell.top + "px";
    box.style.left = cell.left + xOffset + "px";
    box.style.width = actualWidth + "px";
    box.style.height = cell.height + "px";
    box.style.background = "red";
    box.style.borderRadius = "20px"
    document.body.appendChild(box);
}

// Getting data from file
fetch('/output.json')
    .then(response => { return response.json(); })
    .then(data => {
        console.log(data);
        // Going through each dict in data and drawing boxes
        data.forEach(item => {
            let bay = item.bay;
            let time = item.end_date_time;
            time = new Date(time);
            drawBoxOverCells(bay, time, item.category);
        });
    })
    .catch(error => console.error('Error fetching JSON:', error));
