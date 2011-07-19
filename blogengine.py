from flask import Flask, render_template, request, redirect, url_for, abort, session
import default_settings
from flaskext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)   
app.config.from_pyfile('default_settings.py')
db = SQLAlchemy(app)

#the Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    post_body = db.Column(db.Text)
  
    
    def __init__(self, title, post_body, date_published):
        self.title = title
        self.post_body = post_body
   

def initdb():
    db.create_all()
    print "Initialized new empty database in %s" % app.config['SQLALCHEMY_DATABASE_URI']
    

#admin model- need to create a login system        
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/register', methods = ['GET','POST'])
def register():
    if Admin.query.first():
        abort(401) #only one admin can exist
        
    if request.method == 'GET':
        return render_template('register.html')
        
    username = request.form['username']
    password = request.form['password']
    
    if request.form['action'] == 'Register':
        admin = Admin(username, password)
        db.session.add(admin)
        db.session.commit()
        
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    username = request.form['username']
    password = request.form['password']
    
    if request.form['action'] == 'Login':
        admin = Admin.query.first()
        if admin.username != username: error='Invalid Username'
        elif admin.password != username: error='Invalid Password'
        
        else: 
            session['logged_in'] = True
            return redirect(url_for('compose'))    
    
    return render_template('login.html', error = error)
    
@app.route('/logout')
def logout():
    session['logged_in']=False
    return redirect(url_for('index'))
    

#need to add more data- date/time, categories, and some fancy stuff maybe 
@app.route('/compose', methods = ['POST', 'GET'])    
def compose():
    if not session.get('logged_in'):
        abort(401)
        
    if request.method == 'GET':
        return render_template('compose.html')
        
    title = request.form['title']
    post_body = request.form['post_body']
    
    
    if request.form['action'] == 'Publish':
        post = Post(title, post_body)
        db.session.add(post)
        db.session.commit()
        
    return redirect(url_for('index'))

#need to arrange posts in order of time posted. also need to add features like viewing posts individually, categorically and by month posted        
@app.route('/')
def index():
    admin = Admin.query.all()
    posts = Post.query.all()
    
    return render_template('posts.html', posts = posts)    
    
if __name__ == '__main__':
    app.run()
