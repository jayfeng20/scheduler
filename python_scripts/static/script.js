let button = document.querySelector('button');
let weekButton = document.querySelector('.week-page');
let form = document.querySelector('form');
let cells = document.querySelectorAll('td');
let cellNames = document.querySelectorAll('p');

let state = 0;
let taskName;
let week1 = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
];

let week2 = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
];

button.onclick = (event) => {
  event.preventDefault();
  let data = Object.fromEntries(new FormData(form));

  for (const [_, value] of Object.entries(data)) {
    if (value === '') return;
  }

  taskName = data["task-name"];

  $.ajax({
    url: '/process',
    type: 'POST',
    data: {
      'task-name': data["task-name"],
      'task-type': data["task-type"],
      'task-time': data["task-time"],
      'task-due': data["task-due"],
    },
    success: function (response) {
      console.log(response);

      // Update calendar with data
      for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 7; j++) {
          week1[i][j] += response[0][i][j];
          week2[i][j] += response[1][i][j];
        }
      }

      updateCalendar(state === 0 ? week1 : week2);
    },
    error: function (error) {
      console.log(error);
    }
  });
}

function updateCalendar(data) {
  for (let time = 0; time < 8; time++) {
    for (let day = 0; day < 7; day++) {
      if (data[time][day] <= 1) {
        updateCell(time, day);
      } else {
        resetCell(time, day);
      }
    }
  }
}

function updateCell(time, day) {
  cells[time * 7 + day].style.backgroundColor = '#90EE907F';
  cellNames[time * 7 + day].innerText = taskName;
}

function resetCell(time, day) {
  cells[time * 7 + day].style.backgroundColor = '#FFFFFF';
  cellNames[time * 7 + day].innerText = '';
}

weekButton.onclick = (event) => {
  event.preventDefault();

  if (state === 0) {
    weekButton.innerHTML = "Previous Week";
  } else {
    weekButton.innerHTML = "Next Week";
  }
  state = 1 - state;

  updateCalendar(state === 0 ? week1 : week2);
}