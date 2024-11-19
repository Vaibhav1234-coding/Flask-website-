from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from functools import wraps
app=Flask(__name__,template_folder
="template")
app.secret_key="@1234#@"
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False 
db=SQLAlchemy(app)
class users(db.Model):
	id=db.Column("id", db.Integer,primary_key=True)
	name=db.Column(db.String(100))
	email=db.Column(db.String(100))
	def __init__(self, name, email):
		self.name=name
		self.email=email		
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
@app.route("/home")
@login_required
def home():
	return render_template("home.html")
@app.route("/view")
def view():
	return render_template("view.html",values=users.query.all())
@app.route("/login",methods=["GET","POST"])
@login_required
def login():
	if request.method=="POST":
		username=request.form[ 'username']
		session["username"]=username
		found=users.query.filter_by(name=username).first()
		if found:
			session["email"]=found.email
		else:
			usr=users(username, None)
			db.session.add(usr)
			db.session.commit()			
		flash("Login sucessfully")
		return redirect(url_for("user"))
	else:
		if "username" in session:
			flash("Already logged in!")
			return redirect(url_for("user"))	
		return render_template("login.html")
@app.route("/user",methods=["GET","POST"])
def user():
	email=None
	if "username" in session:
		username=session["username"]
		
		if request.method =="POST":
			email=request.form["email"]
			session["email"]=email
			found=users.query.filter_by(name=username).first()
			found.email = email
			db.session.commit()
			flash("Email was saved")
		else:
			if "email"in session:
				email=session["email"]
		return render_template("user.html",email= email)
	else: 
		flash("you are not login in")
		return redirect(url_for("login"))		
@app.route("/logout")
@login_required
def logout():
	flash("You have been logout!")
	session.pop("username", None)
	session.pop("email", None)
	return redirect(url_for("login"))
@app.route("/delete")
def delete():
	if "username" in session:
		username = session["username"]
		found=users.query.filter_by(name=username).all()
		for us in found:
			db.session.delete(us)
		db.session.commit()
		flash("user deleted")
		return redirect(url_for("login"))
	else:
		flash("you are not logged in")
		return redirect(url_for("login"))
@app.route("/")
def admin():
	return redirect(url_for("home"))
if __name__ =="__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)
	
