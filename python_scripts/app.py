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


    # start_times is a list of python datetime objects that represent the start times of the already exisiting timeslots
    # end_times is a list of python datetime objects that represent the end times of the already exisiting timeslots
    # so start_times[0] and end_times[0] forms 1 already existing timeslot
    # same thing for new_start_times, new_end_times but they represent the newly generated timeslots.
    start_times, end_times, new_start_times, new_end_times = test.run()


    # alr_booked_start, alr_booked_end, new_start, new_end = test.run()
    # print(alr_booked_start, alr_booked_end, new_start, new_end)
    # dt1 = datetime.datetime(2023, 12, 21, 9)
    # dt2 = datetime.datetime(2023, 12, 21, 17)

    return f.create_calendar(dt1, dt2)

if __name__ == '__main__':
    app.run(port=5000, debug=True)