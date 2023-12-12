import json
import os
from flask import Flask, render_template, request, jsonify
from random import randint
from subprocess import call, check_output

import userInput

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
    return "done"

if __name__ == '__main__':
    app.run(port=5000, debug=True)