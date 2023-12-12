let button = document.querySelector('button');
let form = document.querySelector('form');
let cells = document.querySelectorAll('td');
let cellNames = document.querySelectorAll('p');

let taskName;

button.onclick = (event) => {
  event.preventDefault();
  let data = Object.fromEntries(new FormData(form));

  for (const [_, value] of Object.entries(data)) {
    if (value === '') return;
  }

  taskName = data["task-name"];

  // Get data from AI (TODO)

  // Update calendar with data
  let calendarData = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
  ];

  updateCalendar(calendarData);
}

function updateCalendar(data) {
  for (let time = 0; time < 8; time++) {
    for (let day = 0; day < 7; day++) {
      if (data[day][time] === 1) {
        updateCell(day, time);
      }
    }
  }
}

function updateCell(day, time) {
  cells[day * 7 + time].style.backgroundColor = '#90EE907F';
  cellNames[day * 7 + time].innerText = taskName;
}