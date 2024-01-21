var scrub = {
    el: document.getElementById("scrub"),
    current: {
      x: 0,
    },
    last: {
      x: 0,
    },
  },
  timeline = document.getElementById("timeline"),
  mouseDown = false;
scrub.el.onmousedown = function (e) {
  mouseDown = true;
  scrub.origin = timeline.offsetLeft;
  scrub.last.x = e.clientX;
  return false;
};

/*scrub.el.onmousedown = function () {
  mouseDown = true;
  scrub.origin = timeline.offsetLeft;
  scrub.last.x = scrub.el.offsetLeft;
  return false;
};
*/
current_position = 0;
document.onmousemove = function (e) {
  if (mouseDown === true) {
    var scrubStyle = getComputedStyle(scrub.el),
      scrubOffset = parseInt(scrubStyle.width, 10) / 2,
      position = parseInt(scrubStyle.left, 10),
      newPosition = position + (e.clientX - scrub.last.x),
      timeStyle = getComputedStyle(timeline, 10),
      timeWidth = parseInt(timeStyle.width, 10);
    if (e.clientX < timeline.offsetLeft) {
      newPosition = scrub.origin - scrubOffset * 2;
    } else if (e.clientX > timeWidth + timeline.offsetLeft) {
      newPosition = timeWidth - scrubOffset;
    }
    current_position = newPosition;
    hour = newPosition * 0.2;
    if (newPosition > 1858) {
      day =
        (Math.floor((hour * 60) / 720) % 30) +
        "  November"; /* There is 60 days total and 270 hours*/
    } else {
      day =
        Math.floor((hour * 60) / 720) +
        "  October"; /* There is 60 days total and 270 hours*/
    }
    hour_of_day = Math.floor(hour % 12) + 7;
    if (hour_of_day < 12) {
      hour_of_day += "am";
    } else {
      hour_of_day += "pm";
    }
    document.getElementById("date_output").value = `${day}  ${hour_of_day}`;
    scrub.el.style.left = newPosition + "px";
    scrub.last.x = e.clientX;
  }
};

document.onmouseup = async function () {
  mouseDown = false;
  schedule_thingie = update_schedule();
  getDataAtSnapshot(schedule_thingie).then((data) => {
    console.log(data);
    findTarget(data, currentDate);
  });
};

function update_schedule() {
  hour = current_position * 0.2;
  day = Math.floor((hour * 60) / 720); /* There is 60 days total and 270 hours*/
  hour_of_day = Math.floor(hour % 12) + 7;
  month = "";
  if (day > 30) {
    month = "11";
    day = day % 30;
  } else {
    month = "10";
  }
  day = Math.max(Number(day), 1);
  day = day < 10 ? "0" + day : "" + day;
  hour_of_day = hour_of_day < 10 ? "0" + hour_of_day : "" + hour_of_day;
  formatted_day = `2022-${month}-${day}/${hour_of_day}:00`;
  return formatted_day;
}
