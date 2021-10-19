from flask import Flask
from flask import render_template
from helper.db import db_init

app = Flask(__name__)


@app.route("/")
def home():
    data = db_init()
    return render_template('main.html', wl_data=list(data['test'].values())[-10:], img_data=[])
