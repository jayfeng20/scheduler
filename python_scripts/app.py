import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from random import randint

# os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html',title="HOMEPAGE")

if __name__ == '__main__':
    app.run(port=5000, debug=True)