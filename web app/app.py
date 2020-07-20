from flask import Flask, render_template, redirect, jsonify, request
from flask_restful import Api, Resource
import pickle
import pandas as pd
import numpy as np
import traceback
import os

#with open("models/model.pkl", "r") as m:
    #model = pickle.load(m)

#with open("models/features.pkl", "r") as f:
    #features = pickle.load(f)

app = Flask(__name__)
#api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")



# predict endpoint
#class Predict_churn(Resource):
#    def post(self):
#
#        if request.method == "POST":
#            try:
#



port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(port = port, debug = True)
