# views.py

from flask import render_template, flash, request, redirect
from flask.wrappers import Request
from app import app, db
from app.models import Order, User, Book
from .forms import AddToBasketForm, ChangePasswordForm, BookForm, SignupForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# @app.route('/', methods=['GET', 'POST'])
# def home():
# 	movies = Movie.query
# 	rows = movies.count()
# 	if current_user.is_authenticated:
# 		watchlist_form = WatchlistForm()
# 		associations = Association.query
# 		user = User.query.filter_by(email=current_user.email).first()
# 		default = 0
# 		if request.method == "POST":
# 			if watchlist_form.status.data == 'watched':
# 				assoc = Association(watched=1)
# 				movie = Movie.query.filter_by(id=watchlist_form.id.data).first()
# 				if movie:
# 					assoc.movie = movie
# 					user.movies.append(assoc)
# 					db.session.add(assoc)
# 					db.session.commit()
# 					flash("Successfully added the movie to watched!")
# 					return render_template('home.html', title='Home', movies=movies, default=default,
# 			rows=rows, user=user, associations=associations, watchlist_form=watchlist_form)
# 				else:
# 					flash("Couldn't find that movie!")
# 					return redirect('/')
# 			elif watchlist_form.status.data == 'not_watched':
# 				assoc = Association(watched=0)
# 				movie = Movie.query.filter_by(id=watchlist_form.id.data).first()
# 				if movie:
# 					assoc.movie = movie
# 					user.movies.append(assoc)
# 					db.session.add(assoc)
# 					db.session.commit()
# 					flash("Successfully removed the movie from watched!")
# 					return redirect('/')
# 				else:
# 					flash("Couldn't find that movie!")
# 					return redirect('/')
# 		else:
# 			return render_template('home.html', title='Home', movies=movies, default=default,
# 			rows=rows, user=user, associations=associations, watchlist_form=watchlist_form)
# 	else:
# 		return render_template('home.html', title='Home', movies=movies, rows=rows)

@app.route('/', methods=['GET', 'POST'])
def home():
	books = Book.query
	rows = books.count()
	if current_user.is_authenticated:
		user = User.query.filter_by(email=current_user.email).first()
		form = AddToBasketForm()
		if form.validate_on_submit():
			book_to_add = Book.query.get(form.id.data)
			if book_to_add:
				order = Order()
				order.book = book_to_add
				user.books.append(order)
				db.session.add(order)
				db.session.commit()
				flash("Successfully added the book to basket!")
				return redirect('/')
			else:
				flash("Couldn't find that book!")
				return redirect('/')
		else:
			return render_template('home.html', title='Home', home=home, books=books, rows=rows, form=form)
	else:
		return render_template('home.html', title='Home', books=books, rows=rows)

# {% if current_user.is_authenticated %}
# 	<form action="" method="post" name="add_btn">
# 		{{ form.id(value=book.id, hidden=True) }}
# 		{{ form.status(value='watched', hidden=True) }}
# 		<input type="submit" class="btn btn-success" value="Add to Basket!">
# 	</form>
# {% endif %}

@app.route('/search', methods=['GET', 'POST'])
def search():
	return 'Search'

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
	if current_user.email == 'sc20ccp@leeds.ac.uk': #only for admin
		form = BookForm()
		if form.validate_on_submit():
			new_book = Book(title=form.title.data, author=form.author.data, photo=form.photo.data, 
			category=form.category.data, stock=form.stock.data, price=form.price.data)
			books = Book.query
			for book in books:
				if book.title == new_book.title:
					flash('That book has already been added!')
					return redirect('/add_book')
			db.session.add(new_book)
			db.session.commit()
			flash('Succesfully added book!')
			return redirect('/add_book')
		else:
			return render_template('add_book.html', title='Add book', form=form)
	else:
		flash('Only admin can add book!')
		return redirect('/')

@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
	user = User.query.filter_by(email=current_user.email).first()
	books = Order.query.filter_by(userId=user.id).all()
	# rows = books.count()
	rows = 2
	return render_template('basket.html', title='Basket', rows=rows, books=books)

# Account related views
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successful!")
				return redirect('/')
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
		login_user(new_user)
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
