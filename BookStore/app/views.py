# views.py

from flask import render_template, flash, request, redirect
from flask.helpers import url_for
from flask.wrappers import Request
from app import app, db
from app.models import Order, User, Book, Category
from .forms import BasketForm, CategoryForm, ChangePasswordForm, BookForm, SearchForm, SignupForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s]:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('appinfo.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

@app.route('/', methods=['GET', 'POST'])
def index():
	logger.info('Index route request')
	categories = Category.query
	form = CategoryForm()
	if request.method == "POST":
		category = Category.query.get(form.id.data)
		return redirect(url_for('category', name=category.name))
	else:
		return render_template('home.html', title='Home', categories=categories, form=form)

@app.route('/category/<name>', methods=['GET', 'POST'])
def category(name):
	logger.info('Category "' + name + '" route request')
	books = Book.query.filter_by(category=name).all()
	rows = len(books)
	if current_user.is_authenticated:
		user = User.query.filter_by(email=current_user.email).first()
		form = BasketForm()
		if request.method == "POST":
			orders = Order.query
			same_order = 0
			for order in orders:
				if order.userId == user.id and order.bookId == form.id.data:
					current_order = order
					current_book = Book.query.filter_by(id=form.id.data).first()
					same_order = 1
			if same_order == 1:
				current_order.quantity += 1
				if current_order.quantity > current_book.stock:
					flash("Not enough books in stock!")
					logger.warning('Tried to add more books than the number in stock')
					return redirect(url_for('category', name=name))
				db.session.commit()
				flash("Successfully added the book to basket!")
				logger.info('User "' + current_user.name + '" added book "' + current_book.title + '" to basket' )
				return redirect(url_for('category', name=name))
			else:
				book_to_add = Book.query.get(form.id.data)
				if book_to_add:
					order = Order(quantity = 1)
					order.book = book_to_add
					user.books.append(order)
					db.session.add(order)
					db.session.commit()
					flash("Successfully added the book to basket!")
					logger.info('User "' + current_user.name + '" added book "' + book_to_add.title + '" to basket' )
					return redirect(url_for('category', name=name))
				else:
					flash("Couldn't find that book!")
					logger.error('Book "' + book_to_add.title + '" could not be found' )
					return redirect(url_for('category', name=name))
		else:
			return render_template('category.html', title=name, books=books, rows=rows, form=form, 
			name=name)
	else:
		return render_template('category.html', title=name, books=books, rows=rows, name=name)

@app.route('/search/<keyword>', methods=['GET', 'POST'])
def search(keyword):
	if keyword == '_empty_':
		logger.info('Empty search route request')
	else:
		logger.info('Search by keyword "' + keyword + '" route request')
	search = SearchForm()
	form = BasketForm()
	searched_books = []
	if request.method == "POST":
		if search.action.data == 'search':
			searched_word = search.title.data.lower()
			return redirect(url_for('search', keyword=searched_word))
		elif form.action.data == 'add':
			if current_user.is_authenticated:
				searched_word = keyword.lower()
				books = Book.query
				for book in books:
					book_title = book.title.lower()
					book_author = book.author.lower()
					if searched_word in book_title or searched_word in book_author:
						searched_books.append(book)
				rows = len(searched_books)
				user = User.query.filter_by(email=current_user.email).first()
				orders = Order.query
				same_order = 0
				for order in orders:
					if order.userId == user.id and order.bookId == form.id.data:
						current_order = order
						current_book = Book.query.filter_by(id=form.id.data).first()
						same_order = 1
				if same_order == 1:
					current_order.quantity += 1
					if current_order.quantity > current_book.stock:
						flash("Not enough books in stock!")
						logger.warning('Tried to add more books than the number in stock')
						return redirect(url_for('search', keyword=searched_word))
					db.session.commit()
					flash("Successfully added the book to basket!")
					logger.info('User "' + current_user.name + '" added book "' + current_book.title + '" to basket' )
					return redirect(url_for('search', keyword=searched_word))
				else:
					book_to_add = Book.query.get(form.id.data)
					if book_to_add:
						order = Order(quantity = 1)
						order.book = book_to_add
						user.books.append(order)
						db.session.add(order)
						db.session.commit()
						flash("Successfully added the book to basket!")
						logger.info('User "' + current_user.name + '" added book "' + book_to_add.title + '" to basket' )
						return redirect(url_for('search', keyword=searched_word))
					else:
						flash("Couldn't find that book!")
						logger.error('Book "' + book_to_add.title + '" could not be found' )
						return redirect(url_for('search', keyword=searched_word))
	else:
		searched_word = keyword.lower()
		books = Book.query
		for book in books:
			book_title = book.title.lower()
			book_author = book.author.lower()
			if searched_word in book_title or searched_word in book_author:
				searched_books.append(book)
		if keyword == '_empty_':
			rows = -1
		else:
			rows = len(searched_books)
		return render_template('search.html', title='Search', search=search, rows=rows, 
		form=form, books=searched_books, keyword=keyword)

@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
	logger.info('Basket route request')
	user = User.query.filter_by(email=current_user.email).first()
	user_orders = user.books
	books = []
	total = 0
	form = BasketForm()
	for user_order in user_orders:
		book = Book.query.filter_by(id=user_order.bookId).first()
		books.append(book)
		total += user_order.quantity * book.price
	total = round(total, 2)
	rows = len(books)
	if request.method == "POST":
		orders = Order.query
		if form.action.data == 'minus' or form.action.data == 'plus' or form.action.data == 'remove':
			for order in orders:
				if order.userId == user.id and order.bookId == form.id.data:
					current_order = order
					current_book = Book.query.filter_by(id=form.id.data).first()
			if form.action.data == 'minus':
				current_order.quantity -= 1
				logger.info('User "' + current_user.name +
				'" decreased the number of copies for book "' + current_book.title + '" in their basket')
			elif form.action.data == 'plus':
				current_order.quantity += 1
				if current_order.quantity > current_book.stock:
					flash("Not enough books in stock!")
					logger.warning('User "' + current_user.name + '" tried to add more books than the number in stock')
					return redirect('/basket')
				logger.info('User "' + current_user.name + 
				'" increased the number of copies for book "' + current_book.title + '" in their basket')
			elif form.action.data == 'remove':
				current_order.quantity = 0
				logger.info('User "' + current_user.name + 
				'" removed all copies of book "' + current_book.title + '" from basket')
			if current_order.quantity == 0:
				db.session.delete(current_order)
		elif form.action.data == 'finalise':
			for book in books:
				for order in orders:
					if order.bookId == book.id:
						if book.stock >= order.quantity:
							book.stock = book.stock - order.quantity
							db.session.delete(order)
						else:
							flash("Not enough copies of " + book.title + "in stock! Only " + book.stock + " left!")
							logger.error('User "' + current_user.name +
							 '" tried to buy more books than the number in stock')
							return redirect('/basket')
			logger.info('User "' + current_user.name + '" finalised their order')
			flash("Order finalised!")
		db.session.commit()
		return redirect('/basket')
	else:
		return render_template('basket.html', title='Basket', rows=rows, books=books, 
		form=form, user_orders=user_orders, total=total)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
	logger.info('Add Book route request')
	if current_user.email == 'sc20ccp@leeds.ac.uk': #only for admin
		form = BookForm()
		if form.validate_on_submit():
			new_book = Book(title=form.title.data, author=form.author.data, photo=form.photo.data, 
			category=form.category.data, stock=form.stock.data, price=form.price.data)
			books = Book.query
			for book in books:
				if book.title == new_book.title and book.author == new_book.author:
					flash('That book has already been added!')
					logger.warning('Admin tried to add book "' + book.title + '" which already exists')
					return redirect('/add_book')
			db.session.add(new_book)
			category = Category.query.filter_by(name=new_book.category).first()
			category.number += 1
			db.session.commit()
			flash('Succesfully added book!')
			logger.info('Admin successfully added book "' + new_book.title + '"')
			return redirect('/add_book')
		else:
			return render_template('add_book.html', title='Add book', form=form)
	else:
		flash('Only admin can add books!')
		logger.warning('User "' + current_user.name + 
		'" tried to access the "Add Books" page without admin privilegies')
		return redirect('/')

# Account related views
@app.route('/login', methods=['GET', 'POST'])
def login():
	logger.info('Login route request')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successful!")
				logger.info('User "' + current_user.name + '" logged in successfully')
				return redirect('/')
			else:
				pw_error = 'Wrong Password! Try again!'
				logger.warning('User failed to login')
				return render_template('login.html', title='Login', form=form, pw_error=pw_error)
		else:
			em_error = 'Invalid email! Try again!'
			logger.warning('User failed to login')
			return render_template('login.html', title='Login', form=form, em_error=em_error)
	else:
		return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	logger.info('Singup route request')
	form = SignupForm()
	if form.validate_on_submit():
		users = User.query
		for user in users:
			if form.email.data == user.email:
				em_error = 'Email already in use! Please enter a different one!'
				logger.warning('User failed to sign up')
				return render_template('signup.html', title='Sign Up', form=form, em_error=em_error)
		hashed_password = generate_password_hash(form.password_hash.data, "sha256")
		new_user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash('Succesfully signed up!')
		login_user(new_user)
		logger.info('User "' + current_user.name + '" singed up successfully')
		return redirect('/')
	else:
		return render_template('signup.html', title='Sign Up', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	logger.info('Profile route request')
	return render_template('profile.html', title=current_user.name)

@app.route('/pw_change', methods=['GET', 'POST'])
@login_required
def pw_change():
	logger.info('Password change route request')
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=current_user.email).first()
		if check_password_hash(user.password_hash, form.old_password.data):
			user.password_hash = generate_password_hash(form.new_password_hash.data, "sha256")
			db.session.commit()
			flash('Successfully changed password!')
			logger.info('User "' + current_user.name + '" changed their password successfully')
			return redirect('/profile')
		else:
			old_pw_error = 'Old password is incorrect! Try again!'
			logger.warning('User "' + current_user.name + '" failed to change their password')
			return render_template('pw_change.html',title='Change Password', form=form, old_pw_error=old_pw_error)
	else:
		return render_template('pw_change.html',title='Change Password', form=form)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
	logger.info('Delete account route request')
	user = User.query.filter_by(email=current_user.email).first()
	if user:
		logger.info('User "' + current_user.name + '" deleted their account')
		logout_user()
		db.session.delete(user)
		db.session.commit()
		flash("You've successfully deleted your account!")
		redirect('/signup')
	return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logger.info('Logout route request')
	flash("You've been successfully logged out!")
	logger.info('User "' + current_user.name + '" logged out')
	logout_user()
	return redirect('/')

