# ============================================================================
# STANDARD LIBRARY IMPORTS
# ============================================================================
# Built-in Python modules that come with the standard installation

import os  # Provides functions for interacting with the operating system (environment variables, file paths, etc.)
from datetime import date  # Used to work with dates (current date, date arithmetic, etc.)
from functools import \
    wraps  # Provides decorator utilities, commonly used to preserve function metadata when creating decorators

# ============================================================================
# THIRD-PARTY FRAMEWORK - FLASK CORE
# ============================================================================
# Main Flask framework and essential utilities

from flask import (
    Flask,  # Main Flask application class to create the web application instance
    abort,  # Function to abort request processing and return HTTP error codes (404, 403, etc.)
    render_template,  # Renders HTML templates with dynamic data using Jinja2 template engine
    redirect,  # Redirects user to a different URL/endpoint
    url_for,  # Generates URLs for specific view functions by their name (best practice for maintainability)
    flash  # Displays one-time messages to users (success, error, info messages) after redirects
)

# ============================================================================
# FLASK EXTENSIONS - UI & FRONTEND
# ============================================================================
# Extensions that enhance the user interface and frontend functionality

from flask_bootstrap import \
    Bootstrap5  # Integrates Bootstrap 5 CSS framework for responsive design and pre-built UI components
from flask_ckeditor import \
    CKEditor  # Rich text WYSIWYG editor for creating and editing formatted content (blog posts, articles, etc.)
# Generates Gravatar profile images based on user email addresses
import hashlib

# ============================================================================
# FLASK EXTENSIONS - DATABASE (SQLAlchemy)
# ============================================================================
# Database ORM (Object-Relational Mapping) for database operations

from flask_sqlalchemy import SQLAlchemy  # Flask integration for SQLAlchemy ORM to manage database connections and queries
from sqlalchemy import Integer, String, Text, ForeignKey  # Column data types for defining database table schemas
from sqlalchemy.orm import (
    relationship,  # Defines relationships between database tables (one-to-many, many-to-one, many-to-many)
    DeclarativeBase,  # Base class for creating declarative SQLAlchemy models
    Mapped,  # Type annotation for mapped attributes in SQLAlchemy 2.0+ (provides better type hints)
    mapped_column  # Defines mapped columns with enhanced type checking and configuration
)

# ============================================================================
# FLASK EXTENSIONS - AUTHENTICATION & SECURITY
# ============================================================================
# User authentication, session management, and password security

from flask_login import (
    UserMixin,  # Mixin class that provides default implementations for user authentication properties (is_authenticated, is_active, etc.)
    login_user,  # Logs in a user and creates a session
    LoginManager,  # Manages user sessions, handles login/logout, and protects routes that require authentication
    current_user,  # Proxy object that represents the currently logged-in user (accessible in routes and templates)
    logout_user  # Logs out the current user and clears their session
)

from werkzeug.security import (
    generate_password_hash,  # Hashes passwords securely using bcrypt/pbkdf2 before storing in database (prevents storing plain text passwords)
    check_password_hash  # Verifies if a plain text password matches a hashed password (used during login)
)

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================
# Manages environment variables and sensitive configuration

from dotenv import load_dotenv  # Loads environment variables from .env file into os.environ (keeps secrets out of code)

# ============================================================================
# LOCAL APPLICATION IMPORTS
# ============================================================================
# Custom forms and models specific to this application

from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model, UserMixin):
    """
    User model - Represents registered users in the BlogPost.

    Inherits from:
    - db.Model: Makes this a SQLAlchemy database table
    - UserMixin: Provides Flask-Login methods (is_authenticated, is_active, get_id, etc.)

    Relationships:
    - ONE User → MANY BlogPosts (via 'posts' attribute)
    - ONE User → MANY Comments (via 'comments' attribute)

    Usage:
    - Create: user = User(email="...", password="...", name="...")
    - Access posts: user.posts (returns list of BlogPost objects)
    - Access comments: user.comments (returns list of Comment objects)
    """
    __tablename__ = "users"

    # Primary key - unique identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # User data
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships to BlogPost - virtual properties
    posts: Mapped[list["BlogPost"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan")

    # Relationships to Comment - virtual properties
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="comment_author",
        cascade="all, delete-orphan")

    def avatar(self, size=100):
        """Return Gravatar URL for this user"""
        return gravatar_url(self.email, size=size)

    def __repr__(self):
        return f'<User: {self.name}>'


class BlogPost(db.Model):
    """
    BlogPost model - Represents blog articles.

    Relationships:
    - MANY BlogPosts → ONE User (each post has one author via 'author' attribute)
    - ONE BlogPost → MANY Comments (via 'comments' attribute)

    Usage:
    - Create: post = BlogPost(title="...", author=user_object, ...)
    - Access author: post.author (returns User object)
    - Access comments: post.comments (returns list of Comment objects)
    """
    __tablename__ = "blog_posts"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign key - links to User table
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Post content
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Relationship to User - virtual property
    author: Mapped["User"] = relationship(
        back_populates="posts")

    # Relationship to Comments - virtual properties
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="parent_post",
        cascade="all, delete-orphan")

    def __repr__(self):
        return f'<BlogPost: {self.title}>'


class Comment(db.Model):
    """
    Comment model - Represents user comments on blog posts.

    Relationships:
    - MANY Comments → ONE User (each comment has one author via 'comment_author' attribute)
    - MANY Comments → ONE BlogPost (each comment belongs to one post via 'parent_post' attribute)

    Usage:
    - Create: comment = Comment(text="...", comment_author=user_object, parent_post=post_object)
    - Access author: comment.comment_author (returns User object)
    - Access post: comment.parent_post (returns BlogPost object)
    """
    __tablename__ = 'comments'

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign key 1 - links to User (who wrote the comment)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Foreign key 2 - links to BlogPost (which post is commented on)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"), nullable=False)

    # Relationship to User - virtual property
    comment_author: Mapped["User"] = relationship(back_populates="comments")

    # Relationship to BlogPost - virtual property
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")

    # Comment content
    text: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f'<Comment by {self.comment_author.name} on {self.parent_post.title}>'


# Create table
with app.app_context():
    db.create_all()

# TODO: Configure Flask-Login
# Create LoginManager instance
login_manager = LoginManager()

# Initialize LoginManager with app
login_manager.init_app(app)

# Configure login view (where to redirect if not logged in)
login_manager.login_view = 'login'  # Name of your login route


# ===== GRAVATAR HELPER FUNCTION =====
def gravatar_url(email, size=50, default='retro', rating='g'):
    """
    Generate Gravatar URL from email address.

    Args:
        email (str): User's email address
        size (int): Image size in pixels (1-2048), default 100
        default (str): Default image style if no Gravatar exists
            Options: '404', 'mp', 'identicon', 'monsterid', 'wavatar',
                     'retro', 'robohash', 'blank'
        rating (str): Content rating - 'g', 'pg', 'r', 'x'

    Returns:
        str: Gravatar image URL
    """
    # Create MD5 hash of lowercase, stripped email
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()

    # Build and return Gravatar URL
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}"

# Make gravatar_url available in all Jinja templates
app.jinja_env.globals['gravatar'] = gravatar_url

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


def admin_only(f):
    """
        Decorator that aborts with 403 error if user is not admin.
        Shows custom 403 error page.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            abort(403)
        return f(*args, **kwargs)

    return wrapper


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # Get values by input in the form
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
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
            return redirect(url_for(endpoint='login'))
        else:
            # Save user to database
            new_user = User(
                email=email,
                password=password_hashed,
                name=name,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return redirect(url_for(endpoint='get_all_posts'))

    return render_template(template_name_or_list="register.html", form=form)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Get values by input in the form
    if form.validate_on_submit():
        provided_email = form.email.data
        provided_password = form.password.data

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
            return redirect(url_for('get_all_posts', user=user))

    return render_template(template_name_or_list="login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=['GET','POST'])
def show_post(post_id):
    """
        Show individual blog post with comments

        GET: Display post and comment form
        POST: Process new comment submission
        """

    # Get post or return 404 if not found
    requested_post = db.get_or_404(BlogPost, post_id)

    # Add the CommentForm to the route.
    comment_form = CommentForm()

    # Process form submission (POST request)
    if comment_form.validate_on_submit():

        # Check if user is logged in.
        if not current_user.is_authenticated:
            flash(message='You need to login or register to comment.', category='error')
            return redirect(url_for('login'))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()

        flash(message='Comment added successfully!', category='Success')

        return redirect(url_for(endpoint='show_post', post_id=post_id))

    return render_template(
        template_name_or_list="post.html",
        post=requested_post,
        form=comment_form
    )


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):

    post = db.get_or_404(BlogPost, post_id)

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()

        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):

    post_to_delete = db.get_or_404(BlogPost, post_id)

    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False, port=5002)
