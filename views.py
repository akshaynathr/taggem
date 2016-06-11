from flask import Flask, render_template, request,redirect,url_for

import json
app=Flask(__name__)


notification=[{ "item": { "time":123 , "user":"akshay"} }]

notification=json.dumps(notification)

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
            return render_template('login.html')
     

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',notification=notification)


@app.route('/signup')
def signup():
	return redirect(url_for('login'))



