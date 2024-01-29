import { CarType, Car } from "/models/car";
import { getQueryParam } from "/util";
import { ScrubBar } from "/scrub-bar";

const requestDateDisplay = document.getElementById("requested-date");

// Retrieve the selected date from the query parameter
const selectedDate = getQueryParam("selectedDate");
const selectedDateDisplay = document.getElementById("selected-date-display");
selectedDateDisplay.innerText = `Selected Date: ${selectedDate}`;

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
function drawBoxOverCells(row, time, car, reqtime) {
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

let relevantRequests = [];

export async function populateSchedule(reqDate, reqTime, appointmentDate) {
  // Clear previous boxes
  document
    .querySelectorAll("div:has(.overlay-image)")
    .forEach((d) => d.remove());

  const formattedDate = `${reqDate}/${reqTime}`;
  const schedule = await getScheduleAtDate(formattedDate);
  const day = schedule["days"][0][appointmentDate];
  const bays = day.bays;
  for (let bay_num = 0; bay_num < bays.length; bay_num++) {
    const jobs = bays[bay_num]["jobs"];
    for (const job of jobs) {
      drawBoxOverCells(
        bay_num + 1,
        job.start_time,
        new Car(job.car_type),
        job.req_time
      );
    }
  }
}

async function getScheduleAtDate(formattedDate) {
  const res = await fetch(`http://localhost:8080/schedule/${formattedDate}`);
  const data = await res.json();
  return data;
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

// Ran when the page loads
(async function main() {
  // Dummy request just to get the # of relevant requests on the selected date
  const schedule = await getScheduleAtDate(`${selectedDate}/19:00`);
  // We set the # ticks in the scrub bar to the # of relevant requests
  // So we go ahead and count the number of jobs on this day
  const day = schedule["days"][0][selectedDate];
  const bays = day.bays;
  for (let i = 0; i < 10; i++) {
    const jobs = bays[i]["jobs"];
    relevantRequests.push(...jobs);
  }
  relevantRequests.push(...day["unassigned_jobs"]);
  relevantRequests.sort((a, b) => {
    if (a.req_time > b.req_time) {
      return 1;
    } else if (a.req_time < b.req_time) {
      return -1;
    } else {
      return 0;
    }
  });
  // Create the scrub bar (which sets up the # ticks)
  new ScrubBar(relevantRequests, requestDateDisplay);
  const [reqDate, reqTime] = relevantRequests[0].req_time.split(" ");
  // We populate the schedule based on the earliest request time relevant to this date
  populateSchedule(reqDate, reqTime, selectedDate);
  requestDateDisplay.innerText = `${reqDate} ${reqTime}`;
})();
