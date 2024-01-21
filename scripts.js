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
