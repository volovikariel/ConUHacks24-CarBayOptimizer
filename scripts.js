import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';

tippy('[data-tippy-content]');
tippy('button', {
    duration: 0,
    arrow: false,
    delay: [1000, 200]
  });

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