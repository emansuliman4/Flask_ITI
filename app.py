from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Book, Author, User
from forms import *
from datetime import datetime
from flask_login import  login_user, login_required, current_user, logout_user
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'emankey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # SQLite for simplicity
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET'])
    def homepage():
        return render_template('home.html')


    @app.route('/book/')
    def all_books():
        books = Book.query.all()
        return render_template('all_books.html', books=books)

    @app.route('/book/<int:book_id>')
    def book_details(book_id):
        book = Book.query.get_or_404(book_id)
        return render_template('book_details.html', book=book)

    @app.route('/author/<int:author_id>')
    def author_details(author_id):
        author = Author.query.get_or_404(author_id)
        return render_template('author_details.html', author=author)

    @app.route('/add_book', methods=['GET', 'POST'])
    def add_book():
        form = BookForm()
        form.author.choices = [(author.id, author.name) for author in Author.query.all()]
        if form.validate_on_submit():
            book = Book(
                name=form.name.data,
                publish_date=form.publish_date.data,
                price=float(form.price.data) if form.price.data else None,
                appropriate=form.appropriate.data,
                author_id=form.author.data
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('all_books'))
        return render_template('add_book.html', form=form)

    @app.route('/add_author', methods=['GET', 'POST'])
    def add_author():
        form = AuthorForm()
        if form.validate_on_submit():
            author = Author(name=form.name.data)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('all_books'))
        return render_template('add_author.html', form=form)
    
    @app.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
    def edit_author(author_id):
        author = Author.query.get_or_404(author_id)
        form = EditauthorForm()
        form.author_select.choices = [(a.id, a.name) for a in Author.query.all()]
        if form.validate_on_submit():
            author.name = form.new_name.data
            db.session.commit()
            return redirect(url_for('author_details', author_id=author.id))
        
        form.author_select.data = author.id
        form.new_name.data = author.name
        return render_template('edit_author.html', form=form)
    
    @app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
    def edit_book(book_id):
        book = Book.query.get_or_404(book_id)
        form = EditbookForm(obj=book) 
        form.author.choices = [(author.id, author.name) for author in Author.query.all()]
        if form.validate_on_submit():
            book.name = form.name.data
            if isinstance(form.publish_date.data, str):
                book.publish_date = datetime.strptime(form.publish_date.data, '%Y-%m-%d').date()
            else:
                book.publish_date = form.publish_date.data
            book.price = form.price.data
            book.appropriate = form.appropriate.data
            book.author_id = form.author.data
            db.session.commit()
            return redirect(url_for('book_details', book_id=book.id))
        return render_template('edit_book.html', form=form)

    
    @app.route('/delete_author/<int:author_id>', methods=['POST'])
    def delete_author(author_id):
        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('all_books'))
    
    @app.route('/delete_book/<int:book_id>', methods=['POST'])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('all_books'))
    




    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return redirect(url_for('register'))
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return redirect(url_for('register'))
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('home'))

    @app.route('/books')
    @login_required 
    def view_books():
        books = Book.query.all()
        return render_template('books.html', books=books)



    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
