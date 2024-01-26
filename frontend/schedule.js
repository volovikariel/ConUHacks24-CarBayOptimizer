currentday = "";

function toggleTable() {
  var table = document.getElementById("scheduleTable");
  if (table.style.opacity === "1" || table.style.opacity === "") {
    table.style.opacity = "0";
  } else {
    table.style.opacity = "1";
  }
}

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

function reformatDate(inputDate) {
  // Split the input date into month and day
  var parts = inputDate.split("-");
  var month = parseInt(parts[0], 10);
  var day = parseInt(parts[1], 10);

  // Create a new Date object with the current year (you can adjust this as needed)
  var currentDate = new Date();
  var year = "2022";

  // Format the month and day with leading zeros if needed
  var formattedMonth = month < 10 ? "0" + month : "" + month;
  var formattedDay = day < 10 ? "0" + day : "" + day;

  // Create the reformatted date string
  var reformattedDate = year + "-" + formattedMonth + "-" + formattedDay;

  return reformattedDate;
}

var currentDate = reformatDate(selectedDate);
console.log("HERE IT IS: " + currentDate);
