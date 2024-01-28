import { Car } from "/models/car";
import { drawBoxOverCells } from "./pages/schedule/schedule";
class ScrubBar {
  constructor() {
    this.el = document.getElementById("scrub-bar");
    this.registerEventListeners();
  }

  registerEventListeners() {
    this.el.addEventListener("change", (e) => {
      const min = this.el.min;
      const max = this.el.max;
      const val = e.target.val;

      // For now, maybe make it Jan 1st 2022
      const minConsideredDate = 0;
      // Make it be the current date
      const maxConsideredDate = val;
    });
  }
}

let formattedDate = getFormattedDate();
const data = await getDataAtDate("2022-10-17/07:15");
findTarget(data, "2022-10-17");

const scrubBar = new ScrubBar();

function findTarget(jsonData, target) {
  // Clear previous boxes
  document
    .querySelectorAll("div:has(.overlay-image)")
    .forEach((d) => d.remove());
  jsonData = jsonData["days"][0][target];
  let bays = jsonData.bays;
  for (let i = 0; i < 10; i++) {
    let jobs = bays[i]["jobs"];
    jobs.forEach((job) => {
      drawBoxOverCells(
        i + 1,
        job.start_time,
        new Car(job.car_type),
        job.req_time
      );
    });
  }
}

function getFormattedDate(val) {
  let year = 2022;
  let hour = val * 0.2;
  let day = Math.floor(
    (hour * 60) / 720
  ); /* There is 60 days total and 270 hours*/
  let hour_of_day = Math.floor(hour % 12) + 7;
  let month = "";
  if (day > 30) {
    month = "11";
    day = day % 30;
  } else {
    month = "10";
  }
  day = Math.max(Number(day), 1);
  day = day < 10 ? "0" + day : "" + day;
  hour_of_day = hour_of_day < 10 ? "0" + hour_of_day : "" + hour_of_day;
  let formattedDate = `${year}-${month}-${day}/${hour_of_day}:00`;
  return formattedDate;
}

async function getDataAtDate(formattedDate) {
  const res = await fetch(`http://localhost:8080/schedule/${formattedDate}`);
  const data = await res.json();
  return data;
}
