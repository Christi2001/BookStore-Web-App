# views.py

from flask import render_template, flash, request, redirect
from flask.wrappers import Request
from app import app, db
from app.models import User
from .forms import SignupForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/', methods=['GET', 'POST'])
def home():
	home={'description':'Welcome to MovieList!'}
	return render_template('home.html', title='Home', home=home)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user)
				flash("Login Successful!")
				return redirect('/profile')
			else:
				flash("Wrong Password! Try again!")
				return render_template('login.html', title='Login', form=form)
		else:
			flash("Invalid email! Try again!")
			return render_template('login.html', title='Login', form=form)
	else:
		return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		users = User.query
		for user in users:
			if form.email.data == user.email:
				error = 'Email already in use! Please enter a different one!'
				return render_template('signup.html', title='Sign Up', form=form, error=error)
		new_user = User(name=form.name.data, email=form.email.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Succesfully signed up!')
		return redirect('/')
	else:
		return render_template('signup.html', title='Sign Up', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template('profile.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You've been successfully logged out!")
	return redirect('/')


# @app.route('/all_assessments', methods=['GET', 'POST'])
# def all_assessments():
#     # form1,2 are used to retrieve the id of an assessment and the type of button when a button is pushed
#     form1 = IdTypeForm()
#     form2 = IdTypeForm()
#     assessments = Assessment.query
#     # rows is used to check if there are assessments created
#     rows = assessments.count()
#     if request.method == "POST":
#         assessment_to_update = Assessment.query.get(form1.id.data)
#         # check which button was pressed and perform the corresponding action
#         if form2.type.data == "uncompleted":
#             assessment_to_update.status = 1
#         elif form2.type.data == "completed":
#             assessment_to_update.status = 0
#         elif form2.type.data == "delete":
#             db.session.delete(assessment_to_update)
#         try:
#             db.session.commit()
#             return redirect('/all_assessments')
#         except:
#             return redirect('/all_assessments')
#     else:
#         return render_template('all_assessments.html',
#                                 title='All Assessments',
#                                 assessments=assessments,
#                                 form1=form1,
#                                 form2=form2,
#                                 rows=rows)
