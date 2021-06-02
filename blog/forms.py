from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # FileField --> type of field is this, FileAllowed--> is like a validator of what kind of file we want to allow to be uploaded and we can restrict like jpg and png
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email , EqualTo, ValidationError
from blog.models import User

class RegistrationForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm_Password",validators=[DataRequired(),EqualTo("password")]) 
	submit = SubmitField("Sign up")

# this validate_username & validate_email are imported from the FlaskForm
	def validate_username(self, username): 
		user = User.query.filter_by(username = username.data).first()
		if user is not None:        # Means user must be None so that it will not throw the messages
			raise ValidationError("That Username is already taken, Please choose Different name")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError("That Email is already taken, Please try with different email")

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember me")
	submit = SubmitField("Login")	


class UpdateAccountForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	picture = FileField("Update Profile Picture",validators=[FileAllowed(["jpg","png"])])
	submit = SubmitField("Update")

# Now here we only want to run this validation checks if the data that they submit is Different than the current username and email 	
	def validate_username(self, username): 
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user is not None:        # Means user must be None so that it will not throw the messages
				raise ValidationError("That Username is already taken, Please choose Different name")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user is not None:
				raise ValidationError("That Email is already taken, Please try with different email")


class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	submit = SubmitField("Post")

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Request Reset Password")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is None:
			raise ValidationError("There is no account with that email. Please create Account First")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm_Password",validators=[DataRequired(),EqualTo("password")])
	submit = SubmitField("Reset Password")







