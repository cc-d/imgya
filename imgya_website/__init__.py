from flask import Flask, session, g, render_template
from pprint import pprint

app = Flask(__name__)
app.config.from_object('prod_config')

@app.route('/')
def hello_world():
    return 'hi'
