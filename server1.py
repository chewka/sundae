from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap

app = flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login();
	return render_template('login.html')

@app.route('signup')
def signup():
	return render_template('signup.html')

@app.route('home')
def home():
	return redirect('index.html')

if __name__ == '__main__':
	app.run(debug=True)