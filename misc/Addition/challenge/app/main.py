from flask_wtf import FlaskForm
from flask import Flask, render_template, request
from wtforms import Form, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

blacklist = ["import", "os", "sys", ";", "print", "__import__", "SECRET", "KEY", "app", "open", "globals", "proc", "self", "read", "exec"]
maybe_not_maybe_this = "HYPA HYPA"
maybe_this_maybe_not = "DUCTF{3v4L_1s_D4ng3r0u5}"

class CalculatorInput(FlaskForm):
	user_input = StringField('Calculation', validators=[validators.DataRequired()]) 
	submit = SubmitField('Calculate for me')

@app.route("/", methods=["GET", "POST"])
def mainpage():	
	form = CalculatorInput()
	out = ""
	if request.method == 'POST':
		user_input = request.form['user_input']
		
		for items in blacklist:
			if items in user_input:
				out = "Nice try....NOT. If you want to break my code you need to try harder"
			else:
				try:
					# Pass the users input in a eval function so that I dont have to write a lot of code and worry about doing the calculation myself
					out = eval(user_input)
				except:
					out = "You caused an error... because my friend told me showing errors to hackers can be problematic I am not going to tell you what you broke"
		
	return render_template("calculator.html", form=form, out=out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=6969)
