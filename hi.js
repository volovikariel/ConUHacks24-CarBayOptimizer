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
  mouseDown = true;

scrub.el.onmousedown = function () {
  mouseDown = true;
  scrub.origin = timeline.offsetLeft;
  scrub.last.x = scrub.el.offsetLeft;
  return false;
};

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
    document.getElementById("output").value = newPosition;
    scrub.el.style.left = newPosition + "px";
    scrub.last.x = e.clientX;
  }
};

document.onmouseup = function () {
  mouseDown = false;
};
