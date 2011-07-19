from flask import Flask, render_template, request, redirect, url_for, abort, session
import default_settings
from flaskext.sqlalchemy import SQLAlchemy  #, desc
from datetime import datetime

app = Flask(__name__)   
app.config.from_pyfile('default_settings.py')
db = SQLAlchemy(app)

#the Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    post_body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    
    def __init__(self, title, post_body, pub_date):
        self.title = title
        self.post_body = post_body
        self.pub_date = pub_date

def initdb():
    db.create_all()
    print "Initialized new empty database in %s" % app.config['SQLALCHEMY_DATABASE_URI']
          
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
    pub_date = datetime.now()
    
    if request.form['action'] == 'Publish':
        post = Post(title, post_body, pub_date)
        db.session.add(post)
        db.session.commit()
        
    return redirect(url_for('index'))

#need to arrange posts in order of time posted. also need to add features like viewing posts individually, categorically and by month posted        
@app.route('/')
def index():
    
    posts = Post.query.order_by(Post.pub_date.desc())
    #ordered_posts = posts.reverse() ##
    return render_template('posts.html', posts = posts)  
    
@app.route('/post/<int:id>')  
def post(id):
    post = Post.query.filter_by(id=id).first()    
    return render_template('post.html', post = post)
    
if __name__ == '__main__':
    app.run()

