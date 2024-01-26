import { update_schedule } from "./scrollbar";
var car_colors = {
  compact: "#d6ef84",
  medium: "#fbee8a",
  "full-size": "#ef957f",
  "class 1 truck": "#edbe94",
  "class 2 truck": "#6576c6",
};

var car_prices = {
  compact: 150,
  medium: 150,
  "full-size": 150,
  "class 1 truck": 250,
  "class 2 truck": 700,
};

var car_images = {
  compact: "./images/compact.png",
  medium: "./images/medium.png",
  "full-size": "./images/full_size.png",
  "class 1 truck": "./images/class1truck.png",
  "class 2 truck": "./images/class2truck.png",
};
let json_data = getDataAtSnapshot(update_schedule());

export async function getDataAtSnapshot(snapshot) {
  let data;
  const res = await fetch(`http://localhost:8080/schedule/${snapshot}`);
  data = await res.json();
  return data;
}

function getAbsolutePosition(element) {
  var rect = element.getBoundingClientRect();
  return {
    top: rect.top + window.scrollY,
    left: rect.left + window.scrollX,
  };
}

var myTableCell = document.getElementById("testing_cell");
var absolutePosition = getAbsolutePosition(myTableCell);
console.log("hello");

function createOverlayImage(element, carType) {
  var overlayImage = new Image();
  overlayImage.src = car_images[carType]; // Replace with the path to your overlay image
  overlayImage.className = "overlay-image";

  // var position = getAbsolutePosition(element);
  // overlayImage.style.top = "0";
  // overlayImage.style.left = "0";

  element.appendChild(overlayImage);
}

// Get location and dimensions of a cell in the calendar table
function getCellLocation(row, col) {
  let table = document.getElementById("calendar");
  let cell = table.rows[row].cells[col];
  let rect = cell.getBoundingClientRect();
  // Getting scroll offsets
  var scrollLeft = document.documentElement.scrollLeft;
  var scrollTop = document.documentElement.scrollTop;
  return {
    top: rect.top + scrollTop,
    left: rect.left + scrollLeft,
    width: rect.width,
    height: rect.height,
  };
}

// Draw a box over cells depending on the bay, the time and vehicle type
export function drawBoxOverCells(row, time, vehicleType, reqtime) {
  const datified_time = new Date(time);

  let cell = getCellLocation(row, datified_time.getHours() - 5);
  // offset based on the minutes of when the appointment is
  let xOffset = (datified_time.getMinutes() * cell.width) / 60 - cell.width;
  let actualWidth = 0;
  // Getting the amount of time a vehicle needs to be serviced for
  // Cell.width corresponds to 1 hour
  if (
    vehicleType === "compact" ||
    vehicleType === "medium" ||
    vehicleType === "full-size"
  ) {
    actualWidth = 0.5 * cell.width;
  } else if (vehicleType === "class 1 truck") {
    actualWidth = cell.width;
  } else {
    actualWidth = 2 * cell.width;
  }
  // Creating the box
  var box = document.createElement("div");
  box.style.position = "absolute";
  box.style.top = cell.top + "px";
  box.style.left = cell.left + xOffset + "px";
  box.style.width = actualWidth + "px";
  box.style.height = cell.height + "px";
  box.style.background = car_colors[vehicleType];
  box.style.borderRadius = "20px";
  box.addEventListener("click", function () {
    modal.style.display = "block";
    modalContent.style.backgroundColor = car_colors[vehicleType];
    modalContent.innerHTML = `Car type: ${vehicleType} <br> Request time: ${reqtime} <br> Reservation time: ${time}<br> Cost:${car_prices[vehicleType]} `;
  });
  document.body.appendChild(box);

  createOverlayImage(box, vehicleType);
}

// Getting data from file
// fetch("/schedule/yyyy-mm-dd/hh:mm"
// .then(res => res.json())
// .then(data => {
//     console.log(data);
//     data.forEach(item => {
//         let bay = item.bay;
//         let time = item.end_date_time;
//         time = new Date(time);
//         drawBoxOverCells(bay, time, item.category);
//     });
// })
// .catch(error => console.error('Error fetching JSON:', error));

// Get references to modal and buttons
var modal = document.getElementById("myModal");
// var openModalBtn = document.getElementById('openModalBtn');
var closeModalBtn = document.getElementById("closeModalBtn");
var modalContent = document.querySelector(".modal-content");

// Event listeners to show/hide modal
closeModalBtn.addEventListener("click", function () {
  modal.style.display = "none";
});

// Close modal if user clicks outside the modal content
window.addEventListener("click", function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
