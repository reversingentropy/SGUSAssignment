from flask import Flask,jsonify,request,render_template,redirect,url_for
from flask.helpers import make_response
from flask_cors import CORS
from model.User import User
from validation.Validator import *
import re
from model.Iris import Iris
import numpy as np
import pickle
from sklearn.naive_bayes import GaussianNB

app = Flask(__name__)
CORS(app)
@app.route('/login')
def start():
    return render_template("login.html")


@app.route('/verifyUser',methods=['POST'])
def check():
    username = request.form['username'].lower()
    password = request.form['password']
    password = password.encode(encoding='utf-8')
    results = User.loginUser(username,password)
    if "error" in results.keys():
            return render_template("login.html",error= results['error'])        
    else:            
        try:
            userid = User.getUserId(username)
            values = Iris.getValues(userid)
            resp = make_response(render_template("irisPredictionPage.html",user=username,userid=userid,values=values))
            resp.set_cookie('jwt',results['jwt'])
            return resp
        except Exception as err:
            return render_template("login.html",message="Error!")

@app.route('/iris',methods=['POST'])
@login_required
def insertVal():
    userid = request.form['userid']
    user = request.form['username']
    sl = request.form['sl']
    sw = request.form['sw']
    pl = request.form['pl']
    pw = request.form['pw']    
    patternVal = re.compile('^[+]?\d+([.]\d+)?$')    
    if (patternVal.match(sl) == None) or (patternVal.match(sw)  == None) or (patternVal.match(pl)  == None )or (patternVal.match(pw) == None) :
        values = Iris.getValues(userid)
        return render_template("irisPredictionPage.html",user=user,userid=userid,values=values,prediction="Please reenter valid values.")
    else:
        new_model = pickle.load(open("ashwin_model.pkl", 'rb'))
        y_pred= new_model.predict([[sl,sw,pl,pw]])
        prediction = ['Setosa', 'Versicolor', 'Virginica'][(y_pred[0])]
        results = Iris.insertValues(userid,sl,sw,pl,pw,prediction)
        values = Iris.getValues(userid)
        return render_template("irisPredictionPage.html",user=user,userid=userid,values=values,prediction=prediction)

@app.route('/logout')
def logout():
    resp = make_response(redirect("login"))
    resp.delete_cookie('jwt')
    return resp

@app.route('/iris/delete',methods=['POST'])
@login_required
def delVal():
    userid = request.form['userid']
    user = request.form['username']    
    results = Iris.delete(userid)
    values = Iris.getValues(userid)
    return render_template("irisPredictionPage.html",user=user,userid=userid,values=values)
    
@app.route('/signUp')
def register():
    return render_template("register.html")


@app.route('/createUser',methods=['POST'])
def create():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form["doublecheck"]
    results = User.getUser(username)
    patternEmail = re.compile('^[a-zA-Z0-9]+[\.]?[a-zA-Z0-9]+@\w+\.\w+$')    
    patternUsername = re.compile('^[a-zA-Z0-9]{8,20}')
    patternPassword = re.compile('^[a-zA-Z0-9]{8,20}')    
    if len(results) != 0 :
        return render_template("register.html",error= "User already exists.")
    elif password != password2:
        return render_template("register.html",error= "Passwords do not match.")
    elif patternEmail.match(email) == None:
        return render_template("register.html",error= "Enter a valid email.")
    elif patternUsername.match(username) == None:
        return render_template("register.html",error= "Enter a valid username with 8 to 20 characters. (No special characters)")
    elif patternPassword.match(password) == None:
        return render_template("register.html",error= "Password must contain 8 to 20 characters.")
    else:
        username = username.lower()
        User.insertUser(username,email,password)
        return render_template("login.html",error="User created! Please login.")

if __name__ == '__main__': 
    app.run(debug=True)
