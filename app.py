from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import numpy as np
import pandas as pd
from numpy import genfromtxt

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("home.html")

@app.route('/choosetype',methods=['POST','GET'])
@cross_origin()
def type():
    if request.method == 'POST':
        try:
            Type = request.form['type']
            if Type == "Bulk":
                return render_template("bulk.html")
            elif Type == "Single":
                return render_template("index.html")

        except Exception as e:
            print('The Exception message is: ', e)
            return 'Please choose a valid method'


@app.route('/predict_single',methods=['POST','GET'])
@cross_origin()
def single():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Pregnancy=float(request.form['Pregnancy'])
            Glucose = float(request.form['Glucose'])
            BP = float(request.form['BP'])
            SkinThickness = float(request.form['SkinThickness'])
            Insulin = float(request.form['Insulin'])
            BMI = float(request.form['BMI'])
            Age = request.form['Age']
            DiabetesPedigree = request.form['DiabetesPedigree']
            filename = 'modelForPrediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            my_array = [[Pregnancy, Glucose, BP, SkinThickness, Insulin, BMI, DiabetesPedigree, Age]]
            x = np.asarray(my_array, dtype='float64')
            prediction=loaded_model.predict(x)
            print('prediction is', prediction)
            if prediction == 0:
                result = "Negative"
            elif prediction == 1:
                result = "Positive"
            return render_template('results.html',prediction=result)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

@app.route('/predict_bulk',methods=['POST','GET'])
@cross_origin()
def bulk():
    if request.method == 'POST':
        try:
            csv_file = request.form['myFile']
            predict_array = genfromtxt(csv_file, delimiter=',', skip_header=1)
            filename = 'modelForPrediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            prediction = loaded_model.predict(predict_array)
            result =[]
            for i in prediction:
                if i == 0:
                    result.append("Negative")
                elif i == 1:
                    result.append("Positive")
            print(result)
            return render_template('result_bulk.html', prediction=result)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
        # return render_template('results.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app