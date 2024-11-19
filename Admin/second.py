from flask import Blueprint,render_template
second=Blueprint("second",__name__,static_folder="static",template_folder="template")
@second.route("/")
def home():
	return render_template("home.html")
@second.route('/test')
def test():
	return "<h1>testpage</h1>"