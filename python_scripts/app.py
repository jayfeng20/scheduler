import json
import os
from flask import Flask, render_template, request, jsonify
from random import randint
from subprocess import call, check_output
import datetime
from lib import funcs as f

import userInput

import test
# os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST']) 
def process(): 
    taskName = request.form.get('task-name')
    taskType = request.form.get('task-type')
    taskTime = request.form.get('task-time')
    taskDue = request.form.get('task-due') 
    userInput.printInput(taskName, taskType, taskTime, taskDue)

    # alr_booked_start: a list of python Datetime objects that represent the start times of already occupied timeslots on the calendar
    # alr_booked_end: a list of python Datetime objects that represent the end times of already occupied timeslots on the calendar
    # new_start: a python Datetime objects that represent the start time of the newly scheduled task
    # new_end: a list of python Datetime objects that represent the end time of the newly scheduled task

    # alr_booked_start, alr_booked_end, new_start, new_end = test.run()
    # print(alr_booked_start, alr_booked_end, new_start, new_end)
    dt1 = datetime.datetime(2023, 12, 12, 3, 0, 0)
    dt2 = datetime.datetime(2023, 12, 12, 5, 0, 0) 
    return f.create_calendar(dt1, dt2)

if __name__ == '__main__':
    app.run(port=5000, debug=True)