function generate_year_range(start, end) {
  var years = "";
  for (var year = start; year <= end; year++) {
    years += "<option value='" + year + "'>" + year + "</option>";
  }
  return years;
}

start_date = new Date(2022, 9, 1);
currentMonth = start_date.getMonth();
currentYear = start_date.getFullYear();

createYear = generate_year_range(2022, 2022);
document.getElementById("year").innerHTML = createYear;

var calendar = document.getElementById("calendar");

var months = "";
var days = "";

var months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

var $dataHead = "<tr>";
for (dhead in days) {
  $dataHead += "<th data-days='" + days[dhead] + "'>" + days[dhead] + "</th>";
}
$dataHead += "</tr>";

//alert($dataHead);
document.getElementById("thead-month").innerHTML = $dataHead;

const monthSelectorEl = document.querySelector("#date-selectors #month");
const yearSelectorEl = document.querySelector("#date-selectors #year");
showCalendar(currentMonth, currentYear);

function next() {
  currentYear = currentMonth === 11 ? currentYear + 1 : currentYear;
  currentMonth = (currentMonth + 1) % 12;
  showCalendar(currentMonth, currentYear);
}

function previous() {
  currentYear = currentMonth === 0 ? currentYear - 1 : currentYear;
  currentMonth = currentMonth === 0 ? 11 : currentMonth - 1;
  showCalendar(currentMonth, currentYear);
}

function jump() {
  currentYear = parseInt(yearSelectorEl.value);
  currentMonth = parseInt(monthSelectorEl.value);
  showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {
  var firstDay = new Date(year, month).getDay();

  tbl = document.getElementById("calendar-body");

  tbl.innerHTML = "";

  monthSelectorEl.value = month;
  yearSelectorEl.value = year;

  // creating all cells
  var day = 1;
  for (var i = 0; i < 6; i++) {
    var row = document.createElement("tr");

    for (var j = 0; j < 7; j++) {
      if (i === 0 && j < firstDay) {
        cell = document.createElement("td");
        cellText = document.createTextNode("");
        cell.appendChild(cellText);
        row.appendChild(cell);
      } else if (day > daysInMonth(month, year)) {
        break;
      } else {
        cell = document.createElement("td");
        cell.setAttribute("data-date", day);
        cell.setAttribute("data-month", month + 1);
        cell.setAttribute("data-year", year);
        cell.setAttribute("data-month_name", months[month]);

        cell.className = "date-picker";
        var selectedDate = `2022-${padZero(month + 1)}-${padZero(day)}`;

        cell.innerHTML =
          '<a href="/pages/schedule/schedule.html?selectedDate=' +
          selectedDate +
          '">' +
          day +
          "</a>";

        if (
          day === start_date.getDate() &&
          year === start_date.getFullYear() &&
          month === start_date.getMonth()
        ) {
          cell.className = "date-picker selected";
        }
        row.appendChild(cell);
        day++;
      }
    }

    tbl.appendChild(row);
  }
}

function daysInMonth(iMonth, iYear) {
  return 32 - new Date(iYear, iMonth, 32).getDate();
}

function padZero(num) {
  num = num.toString();
  if (num.length < 2) {
    num = "0" + num;
  }
  return num;
}
