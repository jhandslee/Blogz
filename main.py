from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '50-QXZ!6jD'

class Blog(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	entry = db.Column(db.String(120))
	body = db.Column(db.String(600))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, entry, body, owner):
		self.entry = entry
		self.body = body
		self.owner = owner

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	blogs = db.relationship("Blog", backref='owner')

	def __init__(self, username, password):
		self.username = username
		self.password = password

@app.before_request
def require_login():
	allowed_routes = ['login', 'register']
	if request.endpoint not in allowed_routes and 'username' not in session:
		return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user and user.password == password:
			session['username'] = username
			flash("logged in")
			return redirect('/')
		else:
			flash("User password incorrect, or user does not exist", 'error')

	return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']

		# TODO verify validation

		existing_user = User.query.filter_by(username=username).first()
		if not existing_user:
			new_user = User(username, password)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = username
			return render_template('login.html')
		else:
			# TODO mesage
			return '<h1>Duplicate user</h1>'

	return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
def index():

	return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
	
	n_entry = Blog.query.filter().all()
	return render_template('blog.html', title="Blog Entries", n_entry=n_entry)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

	owner = User.query.filter_by(username=session['username']).first()

	if request.method == 'POST':
		entry =	request.form['entry']
		body = request.form['body']
		n_entry = Blog(entry, body, owner)
		db.session.add(n_entry)
		db.session.commit()
		flash("Thanks for your entry")

	blogs = Blog.query.filter_by(owner=owner).all()

	return render_template('newpost.html', title="New Blog Entries", blogs=blogs)

@app.route('/ipost', methods=['POST', 'GET'])
def ipost():
	x_id = request.args.get("id")
	bid = Blog.query.get(x_id)

	return render_template("ipost.html", bid=bid)

@app.route('/logout')
def logout():
	del session['username']
	flash("You are logged out of Blogz site")
	return render_template('login.html')

if __name__ == '__main__':
	app.run()