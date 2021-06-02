from blog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from blog import app, db, bcrypt, mail
import secrets
from PIL import Image
from flask_login import login_user,current_user,logout_user, login_required
from flask_mail import Message
import os

# we can't have same function name for the multiple routes
@app.route("/") # decoraters route are what we type to go into different browser like contact about pages and in flask we create this using route decoraters
@app.route("/home")
def home():
	page = request.args.get("page", 1, type=int) # this are used to show the limited page on the Home screen
	post = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page = 5)
	return render_template('home.html',posts = post)

@app.route("/about") # decoraters route are what we type to go into different browser like contact about pages and in flask we create this using route decoraters
def about():
	return render_template("about.html",title = "About")

@app.route("/register", methods = ['POST','GET']) 
def register():
	if current_user.is_authenticated:  # this will take care of if a user is already log in and then also user click on the log in page then it will redirect to the home page
		return redirect(url_for("home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username = form.username.data,email = form.email.data, password = hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash("Your Account Has been Created, You can now log in", "success")
		return redirect(url_for('login'))
	return render_template('register.html',title = "Registration",form = form)

@app.route("/login",methods = ['POST','GET']) 	 
def login():
	if current_user.is_authenticated:   # this will take care of if a user is already log in and then also user click on the log in page then it will redirect to the home page
		return redirect(url_for("home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is not None and bcrypt.check_password_hash(user.password, form.password.data): # so if the user exit and the password they entered is valid	
			login_user(user,remember=form.remember.data) # we have used this function to log the user in (user-> we have to log in this user)
			# if we are trying to access the thing before the log in for particular option then it will show the next in url and it will direct to the login page and as sson as we log in it will redirect to the page that we are accessing to before log in 
			next_page = request.args.get("next") #  args is the dictionary because you dont want to access the next using the square brackets and key name because if it is doesnt exit then it will throw an error and the next parameter is optional and the advantage of using get method is that it will return none if it doesnt exit
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("Unsuccessfull Login.Please Check your email and password","danger")
	return render_template('login.html',title = "Login",form = form)



@app.route("/logout") 	
def logout():
	logout_user()
	return redirect(url_for('home'))

# FUNCTION USED FOR SAVING THE PICTURE
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_,f_ext = os.path.splitext(form_picture.filename)
	picture_name = random_hex + f_ext
	picture_path = os.path.join(app.root_path, "static/profile_pics",picture_name)
	output_image = (125,125)
	compressed_img = Image.open(form_picture)
	compressed_img.thumbnail(output_image)
	compressed_img.save(picture_path)
	return picture_name

@app.route("/account",methods = ["GET","POST"]) 
@login_required   # so now extension know that login requried to access that route but we are also telling the extension where the login route is created and that is set in init.py file 
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your Account has been Updated","success")
		return redirect(url_for("account")) # we are redirecting because of the post get redirect pattern when we change the data in the field and we reload the page we get the confirmation messgae for reload that is why we are using this to get rid of using the confirmation messsage
											# Bacically our browser is telling us that you are about to a run a another post request when you reload the page 
	elif request.method == "GET":
		form.username.data = current_user.username # it is used to populated the data
		form.email.data = current_user.email
	image_file = url_for("static", filename = "profile_pics/"+current_user.image_file)  
	return render_template("account.html",title = "Account",image_file = image_file,form = form)


@app.route("/post/new",methods = ["GET","POST"]) 	
@login_required
def new_post():		
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash("Your Post has been Created","success")
		return redirect(url_for("home"))

	return render_template("create_post.html",title = "New Post", form = form, legend = "New Post")


@app.route("/post/int:<post_id>") 	
def post(post_id):
	post = Post.query.get_or_404(post_id) # id post of that particular is present then return post or throw the 404 page not found error
	return render_template("post.html",title = "post.title",post = post)


@app.route("/post/int:<post_id>/update",methods = ["GET","POST"]) 	
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Your Post has been Updated!","success")
		return redirect(url_for("post", post_id = post.id))

	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content

	return render_template("create_post.html",title = "Update Post", form = form, legend = "Update Post")


@app.route("/post/int:<post_id>/delete",methods = ["POST"]) 	
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Your Post has been Deleted!","success")
	return redirect(url_for("home"))


@app.route("/user/<string:username>")
def user_post(username):
	page = request.args.get("page", 1, type=int) # this are used to show the limited page on the Home screen
	user = User.query.filter_by(username = username).first_or_404()
	post = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page,per_page = 5)
	return render_template('user_post.html',posts = post, user = user)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("Password Reset Request", sender = "noreply@demo.com", recipients=[user.email])
	msg.body = f""" To Reset your password, visit the following link

{url_for('reset_token', token = token, _external = True)}
If you did not ake this request then simply ignore this email and no change will be made.
"""
	mail.send(msg)

@app.route("/reset_password",methods = ["POST","GET"]) #this route is used for the user to enter the email to request the password reset 
def reset_request():
	if current_user.is_authenticated:   # this will take care of if a user is already log in and then also user click on the log in page then it will redirect to the home page
		return redirect(url_for("home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		send_reset_email(user)
		flash("An email has been Sent with Instructions to you Email","success")
		return redirect(url_for("login"))


	return render_template('reset_request.html',title = "Reset Password", form = form)


@app.route("/reset_password/<token>",methods = ["POST","GET"])
def reset_token(token): # this route is used for the reset the password with token is active
	if current_user.is_authenticated:   # this will take care of if a user is already log in and then also user click on the log in page then it will redirect to the home page
		return redirect(url_for("home"))
	user = User.verify_reset_token(token)

	if user is None:
		flash("This is invalid or expired Token","warning")
		return redirect(url_for("reset_request"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user.password = hashed_pw
		db.session.commit()
		flash("Your Password has been updated, Now you can Log in", "success")
		return redirect(url_for('login'))
	return render_template('reset_token.html',title = "Reset Password", form = form)




 