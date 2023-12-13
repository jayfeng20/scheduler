let button = document.querySelector('button');
let weekButton = document.querySelector('.week-page');
let form = document.querySelector('form');
let cells = document.querySelectorAll('td');
let cellNames = document.querySelectorAll('p');

let state = 0;
let taskName;

let week1Names = [
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
];

let week2Names = [
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
  ['', '', '', '', '', '', ''],
];

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

      updateCalendar(state === 0 ? week1 : week2, state);
    },
    error: function (error) {
      console.log(error);
    }
  });
}

function updateCalendar(data) {
  for (let time = 0; time < 8; time++) {
    for (let day = 0; day < 7; day++) {
      if (data[time][day] >= 1) {
        updateCell(time, day, state);
      } else {
        resetCell(time, day);
      }
    }
  }
}

function updateCell(time, day, state) {
  cells[time * 7 + day].style.backgroundColor = '#90EE907F';
  let currWeek = state === 0 ? week1Names : week2Names;

  if (currWeek[time][day] === '') {
    cellNames[time * 7 + day].innerText = taskName;
    
    if (state == 0) {
      week1Names[time][day] = taskName;
    } else {
      week2Names[time][day] = taskName;
    }
  } else {
    if (state == 0) {
      cellNames[time * 7 + day].innerText = week1Names[time][day];
    } else {
      cellNames[time * 7 + day].innerText = week2Names[time][day];
    }
  }
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