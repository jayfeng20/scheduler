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

print("before runscript")
@app.route("/userInput.py", methods=['GET', 'POST'])
def runscript():
    print("in runscript")
    if request.method == 'POST':
        print("in if statement")
        taskName = request.form.get('task-name')
        taskType = request.form.get('task-type')
        taskTime = request.form.get('task-time')
        taskDue = request.form.get('task-due')
        return userInput.printInput(taskName, taskType, taskTime, taskDue)
 
    else:
        return render_template('index.html')

        

if __name__ == '__main__':
    app.run(port=5000, debug=True)