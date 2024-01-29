import { populateSchedule } from "/pages/schedule/schedule";
export class ScrubBar {
  constructor(relevantRequests, display) {
    this.el = document.getElementById("scrub-bar");
    this.relevantRequests = relevantRequests;
    this.el.min = 1;
    this.el.max = relevantRequests.length;
    this.display = display;
    this.registerEventListeners();
  }

  registerEventListeners() {
    this.el.addEventListener("change", async (e) => {
      const val = e.target.valueAsNumber;
      // We're 1-indexing the scrub-bar, so we need to subtract 1
      const req = this.relevantRequests[val - 1];

      const [reqDate, reqTime] = req.req_time.split(" ");
      const [appointmentDate, _] = req.start_time.split(" ");
      await populateSchedule(reqDate, reqTime, appointmentDate);
      this.display.innerText = req.req_time;
    });
  }
}
