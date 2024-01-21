

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

