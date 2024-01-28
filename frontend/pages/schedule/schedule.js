import { CarType } from "/models/car";

// Function to get query parameter by name
function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}
// Retrieve the selected date from the query parameter
const selectedDate = getQueryParam("selectedDate");
// Display the selected date in the h1 element
document.getElementById(
  "selectedDateDisplay"
).innerText = `Selected Date: ${selectedDate}`;

function createOverlayImage(element, car) {
  var overlayImage = new Image();
  overlayImage.src = car.image;
  overlayImage.className = "overlay-image";

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
export function drawBoxOverCells(row, time, car, reqtime) {
  const datified_time = new Date(time);

  let cell = getCellLocation(row, datified_time.getHours() - 5);
  // offset based on the minutes of when the appointment is
  let xOffset = (datified_time.getMinutes() * cell.width) / 60 - cell.width;
  let actualWidth = 0;
  // Getting the amount of time a vehicle needs to be serviced for
  // Cell.width corresponds to 1 hour
  if (
    car.type === CarType.compact ||
    car.type === CarType.medium ||
    car.type === CarType.fullSize
  ) {
    actualWidth = 0.5 * cell.width;
  } else if (car.type === CarType.class1Truck) {
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
  box.style.background = car.color;
  box.style.borderRadius = "20px";
  box.addEventListener("click", function () {
    modal.style.display = "block";
    modalContent.style.backgroundColor = car.color;
    modalContent.innerHTML = `Car type: ${car.type} <br> Request time: ${reqtime} <br> Reservation time: ${time}<br> Cost:${car.price} `;
  });
  document.body.appendChild(box);

  createOverlayImage(box, car);
}

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
