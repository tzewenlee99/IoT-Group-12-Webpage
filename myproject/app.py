from flask import Flask
from flask import render_template
from helper.db import db_init

app = Flask(__name__)


@app.route("/")
def home():
    data = db_init()
    print(data)
    return render_template('main.html', wl_data=data['water_level'], img_data=data['images'])
