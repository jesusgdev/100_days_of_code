from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Create Database
class Base(DeclarativeBase):
    pass


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define User model - represents the users table in database
class User(db.Model, UserMixin):
    """
        User model with Flask-Login integration

        UserMixin provides these methods automatically:
        - is_authenticated: Returns True if user is logged in
        - is_active: Returns True if user account is active
        - is_anonymous: Returns False (True only for anonymous users)
        - get_id(): Returns the user ID as a string
        """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    def __repr__(self):
        return f'<User: {self.email}>'


# Create table
with app.app_context():
    db.create_all()

# Create LoginManager instance
login_manager = LoginManager()

# Initialize LoginManager with app
login_manager.init_app(app)

# Configure login view (where to redirect if not logged in)
login_manager.login_view = 'login'  # Name of your login route


@login_manager.user_loader
def load_user(user_id):
    """
       This function is called by Flask-Login to load a user from database

       Parameters:
           user_id (str): The user's ID stored in the session

       Returns:
           User object or None if user doesn't exist

       Flask-Login calls this function automatically on every request
       to check if the user is logged in
       """

    return db.session.get(User, int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        message = flash(message="You've already logged in.", category="success")
        return render_template(template_name_or_list='index.html', message=message)

    return render_template(template_name_or_list="index.html")


@app.route(rule='/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get values by input in the form
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_hashed = generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
            salt_length=8
        )

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if user:
            message = flash(message="You've already signed up with that email, log in instead!", category="error")
            return render_template(template_name_or_list='login.html', message=message)
        else:
            # Save user to database
            new_user = User(
                name=name,
                email=email,
                password=password_hashed,
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return render_template(template_name_or_list='secrets.html', user=new_user)

    return render_template(template_name_or_list="register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        provided_email = request.form.get('email')
        provided_password = request.form.get('password')

        user = db.session.scalar(
            db.select(User).where(User.email == provided_email)
        )

        if not user:
            flash(message='That email does not exist, please try again', category='error')
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, provided_password):
            flash(message='Password incorrect, please try again.', category='error')
            return redirect(url_for('login'))

        else:
            login_user(user)
            return render_template(template_name_or_list='secrets.html', user=user)

    return render_template("login.html")


@app.route('/secrets')
@login_required  # Only logged-in users can access
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required  # Only logged-in users can access
def download():
    directory = os.path.join(app.root_path, 'static', 'files')

    filename = 'cheat_sheet.pdf'

    return send_from_directory(
        directory=directory,
        path=filename,
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True)
