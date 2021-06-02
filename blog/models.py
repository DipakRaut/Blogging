from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model,UserMixin): # we have import the Model by db.Model             https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20),unique = True, nullable = False)
	email = db.Column(db.String(200),unique = True, nullable = False) # by using backref = "author" we can access the User information from the Post table
	image_file = db.Column(db.String(20), nullable = False,default = "default.jpg")
	password = db.Column(db.String(50), nullable = False)              # here posts is one to many relationship
	posts = db.relationship("Post",backref = "author", lazy = True)    # declaring Models for relationship https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
																	   # loads the necessary data in one go
	
	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config["SECRET_KEY"], expires_sec) # crested a serialzier
		# it then dumps means with given dictionary payload we assign to the s, then we can retrive the user id by loads method
		return s.dumps({'user_id': self.id}).decode('utf-8') # returning the token which is created by the
	# Method for verify the token dumps method and also it contain the payload of the current user id 

	@staticmethod # bascially we are telling the python not to except an self parameter as an argument and we are only gonna be accepting the token as an argument
	def verify_reset_token(token): # i this we are using the try catch because token could be invalid, or token could be experied
		s = Serializer(app.config["SECRET_KEY"])
		try:
			user_id = s.loads(token)["user_id"]
		except:
			None
		return User.query.get(user_id)


	def __repr__(self):            # this method is usefull to that how our object will be printed0
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(50),nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # utcnow they are consistent
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"

