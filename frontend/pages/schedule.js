import Link from "next/link";

export default function Schedule() {
  return (
    <div>
      <head>
        <meta charset="UTF-8" />
        <title>ConUHacks VIII</title>
        <link rel="stylesheet" href="style.css" />
      </head>
      <body>
        <div class="container">
          <table>
            <thead>
              <tr>
                <th></th>
                <th>7am</th>
                <th>8am</th>
                <th>9am</th>
                <th>10am</th>
                <th>11am</th>
                <th>12pm</th>
                <th>1pm</th>
                <th>2pm</th>
                <th>3pm</th>
                <th>4pm</th>
                <th>5pm</th>
                <th>6pm</th>
                <th>7pm</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Reserved</td>
                <td></td>
              </tr>
              <tr>
                <td>Reserved</td>
                <td></td>
              </tr>
              <tr>
                <td>Reserved</td>
                <td></td>
              </tr>
              <tr>
                <td>Reserved</td>
                <td></td>
              </tr>
              <tr>
                <td>Reserved</td>
                <td></td>
              </tr>
              <tr>
                <td>Compact Cars</td>
                <td></td>
              </tr>
              <tr>
                <td>Medium Cars</td>
                <td></td>
              </tr>
              <tr>
                <td>Full-Size Cars</td>
                <td></td>
              </tr>
              <tr>
                <td>Class 1 Trucks</td>
                <td></td>
              </tr>
              <tr>
                <td>Class 2 Trucks</td>
                <td></td>
              </tr>
            </tbody>
          </table>
          <div>
            <button type="button">View Report</button>
          </div>
          <table class="schedule">
            <tr>
              <th></th>
              <th>Served Customers</th>
              <th>Declined Customers</th>
            </tr>
            <tr>
              <td>Compact Cars</td>
            </tr>
            <tr>
              <td>Medium Cars</td>
              <td></td>
            </tr>
            <tr>
              <td>Full-Size Cars</td>
              <td></td>
            </tr>
            <tr>
              <td>Class 1 Trucks</td>
              <td></td>
            </tr>
            <tr>
              <td>Class 2 Trucks</td>
              <td></td>
            </tr>
          </table>
        </div>
      </body>
      <h1>
        <Link href={"/"}>Pick different date</Link>
      </h1>
    </div>
  );
}
