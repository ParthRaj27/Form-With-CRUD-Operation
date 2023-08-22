from flask import Flask , render_template ,  redirect , request , session 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer
import json

# from flask_mail import Mail , Message
with open('config.json' , 'r') as c:
    params = json.load(c)["params"]
    
    
app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_ECHO'] = True

   
@app.route('/login' , methods = [ 'GET' , 'POST']) 
def Dashboard():
    if ('user' in session and session["user"]==params['AdminUser']):
        data=Data.query.all()
        return render_template("dashboard.html"  , params=params , data=data)
    if request.method=='POST':
        username=request.form.get('username')
        userpass=request.form.get('password')
        if(username == params['AdminUser'] and userpass == params['AdminPass']):
            session['user'] = username
            data=Data.query.all()
            return render_template("dashboard.html"  , params=params , data=data)
    
    return render_template('login.html' , params=params)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


@app.route("/delete/<string:sr>")
def delete(sr):
    if ('user' in session and session["user"]==params['AdminUser']):
        data=Data.query.filter_by(sr=sr).first()
        db.session.delete(data)
        db.session.commit()
    
    return redirect('/')


@app.route("/edit/<string:sr>", methods = [ 'GET' , 'POST'])
def edit(sr):
     if ('user' in session and session["user"]==params['AdminUser']):
         if request.method=='POST':
            name=request.form.get("name")
            enrollment=request.form.get("enrollment")
            branch=request.form.get("branch")
            class2=request.form.get("class")
            number=request.form.get("phone number")
            email=request.form.get("email")
            # date=datatime.now()
            
            if sr=="0":
                data = Data(name=name,enrollment=enrollment,branch=branch,class2=class2,number=number,email=email , date=datetime.now())
                db.session.add(data)
                db.session.commit()
            else:
                data=Data.query.filter_by(sr=sr).first()
                data.name=name
                data.enrollment=enrollment
                data.branch=branch
                data.class2=class2
                data.number=number
                data.email=email
                db.session.commit()
                return redirect('/edit/'+ sr)
     data=Data.query.filter_by(sr=sr).first()    
     return render_template("edit.html" , params=params ,data=data ,sr=sr)
    

@app.route('/login')
def about():
    return render_template('login.html')

# Reference code for logout
# @app.route('/logout')
# def logout():
#     session.pop('user', None)  # Remove the 'user' key from the session
#     return redirect('/')  # Redirect to the home page



class Data(db.Model):
    sr = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    enrollment = db.Column(db.Integer, nullable=False)
    branch = db.Column(db.String(50),nullable=False)
    class2 = db.Column(db.String(50),nullable=False)
    number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(12), default=datetime.utcnow)
    
@app.route('/' , methods = [ 'GET' , 'POST'])
def home():
    return render_template('index.html')

@app.route('/data' , methods = [ 'GET' , 'POST'])
def data():
     if request.method=='POST':
        name=request.form.get('name')
        enrollment =request.form.get('enrollment')
        branch=request.form.get('branch')
        class2=request.form.get('class')
        number=request.form.get('phone number')
        # number=request.form.get('number')
        email=request.form.get('email')
        entry = Data( name=name , enrollment=enrollment , branch=branch , number=number , email=email ,class2=class2, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
     return render_template('index.html')
 





if __name__ == "__main__":
 app.run(debug=True)
    
    
    
    # whenever we are pass arg to the class while connecting to the database then always capitlized first word at the passing time