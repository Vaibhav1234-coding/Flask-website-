from flask import Flask,render_template
from Admin.second import second
app=Flask(__name__,template_folder
="template")
app.register_blueprint(second, url_prefix="/admin")
@app.route("/")
def home():
	return render_template("static index.html")
if __name__ == "__main__":
	app.run(debug=True)