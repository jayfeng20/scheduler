import json
import os
from flask import Flask, render_template, request, jsonify
from random import randint
from subprocess import call, check_output
import datetime
from lib import funcs as f

import userInput

import test2
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
    start_times, end_times, new_start_times, new_end_times = test2.run(task_name=taskName, task_type=taskType, task_time=taskTime, task_due=taskDue)
    print(f"task time is {taskTime}")
    print(f"taks due is {taskDue}")

    calendar = []
    for i in range(len(new_end_times)):
        t1 = new_start_times[i]
        t2 = new_end_times[i]
        calendar.append(f.create_calendar(t1, t2))
        
    return f.add_calendars(calendar)

if __name__ == '__main__':
    try:
        test.drop_table()
    except:
        pass
    app.run(port=3307, debug=True)
