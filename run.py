# from flask import Flask, render_template,url_for,flash,redirect
# from forms import RegistrationForm,LoginForm
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import os
# # >>> db.create_all() it will create the databases
# # 17:10 ----> 4
# # url_for is a function that will find a exact location of routes for us 
# # instained flask application
# app = Flask(__name__) # creating the app variable and setting this to an instance of flask class name is same as main when you run the app
# # app.config["SECRET_KET"] = "8f8d320eb237bed38368d245d4163ec3bd"
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # to setting this location we need to set this as a configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # we are giving the URL for storing the database i.e location of database
# db = SQLAlchemy(app) # Creating the database instances

# class User(db.Model): # we have import the Model by db.Model             https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# 	id = db.Column(db.Integer, primary_key = True)
# 	username = db.Column(db.String(20),unique = True, nullable = False)
# 	email = db.Column(db.String(200),unique = True, nullable = False) # by using backref = "author" we can access the User information from the Post table
# 	image_file = db.Column(db.String(20), nullable = False,default = "default.jpg")
# 	password = db.Column(db.String(50), nullable = False)              # here posts is one to many relationship
# 	posts = db.relationship("Post",backref = "author", lazy = True)    # declaring Models for relationship https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# 																	   # loads the necessary data in one go
# 	def __repr__(self):            # this method is usefull to that how our object will be printed
# 		return f"User('{self.username}','{self.email}','{self.image_file}')"

# class Post(db.Model):
# 	id = db.Column(db.Integer,primary_key = True)
# 	title = db.Column(db.String(50),nullable = False)
# 	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # utcnow they are consistent
# 	content = db.Column(db.Text, nullable = False)
# 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

# 	def __repr__(self):
# 		return f"Post('{self.title}','{self.date_posted}')"

# from models import User, Post


# posts = [

# {
# 		"author": "Dipak Raut",
# 		"title":  "Blog posts 1",
# 		"content":  "Flask",
# 		"date_posted":  "21/05/2021"
# }, 

# {
# 		"author": "Shanu Raut",
# 		"title":  "Blog post 2",
# 		"content":  "Django",	
# 		"date_posted":  "21/05/2027"
# }
 

# ]


# @app.route("/") # decoraters route are what we type to go into different browser like contact about pages and in flask we create this using route decoraters
# @app.route("/home")
# def home():
# 	return render_template('home.html',posts = posts)

# @app.route("/about") # decoraters route are what we type to go into different browser like contact about pages and in flask we create this using route decoraters
# def about():
# 	return render_template('about.html',title = "About")

# @app.route("/register", methods = ['POST','GET']) 
# def register():
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		flash(f"Accounted Created for {form.username.data}!", "success")
# 		return redirect(url_for('home'))
# 	return render_template('register.html',title = "Registration",form = form)

# @app.route("/login",methods = ['POST','GET']) 	
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		if form.email.data == "admin@gmail.com" and form.password.data == "1443":
# 			flash("Log in Successful", "success")
# 			return redirect(url_for('home'))
# 		else:
# 			flash("Unsuccessfull Login.Please Check your email and password","danger")
# 	return render_template('login.html',title = "Login",form = form)


# dipaknikeeta1443@gmail.com




from blog import app

if __name__ =="__main__":
	app.run(debug = True)

