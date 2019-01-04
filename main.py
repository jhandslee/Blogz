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

	def __init__(self, entry, body):
		self.entry = entry
		self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
	return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

	n_entry = Blog.query.filter().all()
	return render_template('blog.html', title="Blog Entries", n_entry=n_entry)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
	if request.method == 'POST':
		entry =	request.form['entry']
		body = request.form['body']
		n_entry = Blog(entry, body)
		db.session.add(n_entry)
		db.session.commit()
		flash("Thanks for your entry")

	blogs = Blog.query.filter().all()
	return render_template('newpost.html', title="New Blog Entries", blogs=blogs)

if __name__ == '__main__':
	app.run()