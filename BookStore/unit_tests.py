# unit_tests.py

import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
from werkzeug.security import generate_password_hash, check_password_hash

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        db.session.remove()
        hashed_password = generate_password_hash('password123', "sha256")
        admin = models.User(name = 'Christian Constantin Pustianu', email = 'sc20ccp@leeds.ac.uk', 
        password_hash = hashed_password)
        db.session.add(admin)
        db.session.commit()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_search_page(self):
        no_keyword = self.app.get('/search', follow_redirects=True)
        self.assertEqual(no_keyword.status_code, 404)
        
        random_keyword = self.app.get('/search/dadlkfmaldfm', follow_redirects=True)
        self.assertEqual(random_keyword.status_code, 200)
        
        default_keyword= self.app.get('/search/anything', follow_redirects=True)
        self.assertEqual(default_keyword.status_code, 200)
    
    def test_category_page(self):
        no_category = self.app.get('/category', follow_redirects=True)
        self.assertEqual(no_category.status_code, 404)
        
        random_category = self.app.get('/category/hello', follow_redirects=True)
        self.assertEqual(random_category.status_code, 200)
        
        chosen_category= self.app.get('/search/Drama', follow_redirects=True)
        self.assertEqual(chosen_category.status_code, 200)
    
    def test_signup(self):
        signup = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(signup.status_code, 200)
        user = models.User(name='John Doe', email= 'johndoe@yahoo.com', password='john123')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.name, 'John Doe')
        self.assertNotEqual(user.name, 'John')
    
    def test_login(self):
        login = self.app.get('/login', follow_redirects=True)
        self.assertEqual(login.status_code, 200)
        user = models.User.query.filter_by(email='sc20ccp@leeds.ac.uk').first()
        self.assertEqual(user.name, 'Christian Constantin Pustianu')
        self.assertNotEqual(user.name, 'Chris')
        # test hashing
        self.assertTrue(check_password_hash(user.password_hash, 'password123'))
        self.assertFalse(check_password_hash(user.password_hash, 'password'))
    
    def test_orders(self):
        basket = self.app.get('/basket', follow_redirects=True)
        self.assertEqual(basket.status_code, 200)
        
        user = models.User.query.filter_by(email='sc20ccp@leeds.ac.uk').first()
        self.assertEqual(user.name, 'Christian Constantin Pustianu')
        
        book_to_add1 = models.Book(title = 'Hunger Games', author = 'Suzanne Collins', 
        photo = 'hunger_games.jpg', category = 'Action and Adventure', stock = '50', price = '19.99')
        db.session.add(book_to_add1)
        self.assertEqual(book_to_add1.title, 'Hunger Games')

        book_to_add2 = models.Book(title = 'Hamlet', author = 'Shakespeare', 
        photo = 'hamlet.jpg', category = 'Drama', stock = '40', price = '4.99')
        db.session.add(book_to_add2)
        self.assertEqual(book_to_add2.category, 'Drama')
        self.assertNotEqual(book_to_add2.category, 'Anthology')
        
        order1 = models.Order(quantity = 1)
        order1.book = book_to_add1
        user.books.append(order1)
        db.session.add(order1)
        db.session.commit()
        self.assertEqual(order1.id, 1)
        self.assertEqual(order1.bookId, 1)
        self.assertEqual(order1.userId, 1)
        self.assertEqual(order1.quantity, 1)

        books = models.Book.query.all()
        for order in user.books:
            for book in books:
                if order.bookId == book.id:
                    self.assertEqual(book.title, 'Hunger Games')
                    self.assertEqual(book.price, 19.99)
                    self.assertEqual(order.quantity, 1)
        self.assertEqual(len(user.books), 1)
        
        order2 = models.Order(quantity = 1)
        order2.book = book_to_add2
        user.books.append(order2)
        db.session.add(order2)
        db.session.commit()
        self.assertEqual(order2.bookId, 2)
        self.assertEqual(len(user.books), 2)
        
        db.session.delete(order1)
        db.session.commit()
        self.assertEqual(len(user.books), 1)
        
        db.session.delete(order2)
        db.session.commit()
        self.assertEqual(len(user.books), 0)


if __name__ == "__main__":
    unittest.main()