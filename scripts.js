

var boxElement = document.createElement("div")

boxElement.style.width = "130px";
boxElement.style.height = "80px";
boxElement.style.display = "inline-block";
boxElement.style.backgroundColor = "#f00";
boxElement.style.marginLeft = "190px";
boxElement.style.marginTop = "280px"
boxElement.style.position = "relative"
boxElement.style.zIndex = "1";
boxElement.style.borderRadius = "10px";

document.body.appendChild(boxElement)
for (let index = 0; index < 10; index++) {
    let boxElement = document.createElement("div")
    let marginTop = -75.75 + 4.4 * index;
    console.log( marginTop + "%");
    boxElement.style.width = "130px";
    boxElement.style.height = "70px";
    boxElement.style.display = "inline-block";
    boxElement.style.backgroundColor = "#f00";
    boxElement.style.marginLeft = "8%";
    boxElement.style.marginTop = marginTop + "%";
    boxElement.style.position = "absolute";
    boxElement.style.zIndex = "1";
    boxElement.style.borderRadius = "10px";
    document.body.appendChild(boxElement)
}

function getAbsolutePosition(element) {
    var rect = element.getBoundingClientRect();
    return {
      top: rect.top + window.scrollY,
      left: rect.left + window.scrollX
    };
  }
  var myTableCell = document.getElementById('testing_cell');
    var absolutePosition = getAbsolutePosition(myTableCell);
    console.log("hello")
    console.log('Absolute Position:', absolutePosition);

    function createOverlayImage(element) {
        var overlayImage = new Image();
        overlayImage.src = 'mechanic.png'; // Replace with the path to your overlay image
        overlayImage.className = 'overlay-image';
  
        var position = getAbsolutePosition(element);
        overlayImage.style.top = '0';
        overlayImage.style.left = '0';
  
        element.appendChild(overlayImage);
      }
  
createOverlayImage(myTableCell)

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
