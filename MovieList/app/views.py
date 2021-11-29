# views.py

from flask import render_template, flash, request, redirect
from flask.wrappers import Request
from app import app, db
from app.models import User
from .forms import ChangePasswordForm, SignupForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

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
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successful!")
				return redirect('/profile')
			else:
				pw_error = 'Wrong Password! Try again!'
				return render_template('login.html', title='Login', form=form, pw_error=pw_error)
		else:
			em_error = 'Invalid email! Try again!'
			return render_template('login.html', title='Login', form=form, em_error=em_error)
	else:
		return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		users = User.query
		for user in users:
			if form.email.data == user.email:
				em_error = 'Email already in use! Please enter a different one!'
				return render_template('signup.html', title='Sign Up', form=form, em_error=em_error)
		hashed_password = generate_password_hash(form.password_hash.data, "sha256")
		new_user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash('Succesfully signed up!')
		login_user(user)
		return redirect('/')
	else:
		return render_template('signup.html', title='Sign Up', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template('profile.html', title=current_user.name)

@app.route('/pw_change', methods=['GET', 'POST'])
@login_required
def pw_change():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=current_user.email).first()
		if check_password_hash(user.password_hash, form.old_password.data):
			user.password_hash = generate_password_hash(form.new_password_hash.data, "sha256")
			db.session.commit()
			flash('Successfully changed password!')
			return redirect('/profile')
		else:
			old_pw_error = 'Old password is incorrect! Try again!'
			return render_template('pw_change.html',title='Change Password', form=form, old_pw_error=old_pw_error)
	else:
		return render_template('pw_change.html',title='Change Password', form=form)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
	user = User.query.filter_by(email=current_user.email).first()
	if user:
		logout_user()
		db.session.delete(user)
		db.session.commit()
		flash("You've successfully deleted your account!")
		redirect('/signup')
	return redirect('/')

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
