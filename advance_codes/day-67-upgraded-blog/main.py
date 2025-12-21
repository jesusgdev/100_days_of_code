from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

# Form for create a new post.
class NewPostForm(FlaskForm):
    title = StringField(
        'Blog Post Title',
        validators=[
            DataRequired(message='The title is required'),
            Length(min=5, max=250, message='The title must be between 5 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    subtitle = StringField(
        'Subtitle',
        validators=[
            DataRequired(message='The subtitle is required'),
            Length(min=5, max=250, message='The subtitle must be between 5 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    author = StringField(
        'Your Name',
        validators=[
            DataRequired(message="The Author's name is required"),
            Length(min=5, max=250, message="The author's name must be between 5 and 250 characters")
        ],
        render_kw={'class': 'form-control'}
    )
    img_url = StringField(
        'Blog Image URL',
        validators=[
            DataRequired(message="The image url is required"),
            Length(min=5, max=250, message='The image url must be between 5 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    body = CKEditorField (
        'Blog Content',
        validators=[
            DataRequired(message="The Blog content is required"),
            Length(min=500, max=8000, message='The image url must be between 500 and 8000 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(label='Submit Post', render_kw={'class': 'btn btn-primary'})

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.

    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/<int:post_id>')
def show_post(post_id):

    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.get(entity=BlogPost, ident=post_id)
    return render_template("post.html", post=requested_post)

# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=['GET','POST'])
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():

        # Get the data from form and create a new post
        _new_post = BlogPost (
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y"),
        )

        # Add to database and save
        db.session.add(_new_post)
        db.session.commit()

        return redirect(url_for('get_all_posts'))

    return render_template(template_name_or_list="make-post.html", form=form)

# TODO: edit_post() to change an existing blog post
@app.route("/edit/<int:post_id>", methods=['GET','POST'])
def edit_post(post_id):

    # Find post in database by ID
    existing_post = db.get_or_404(entity=BlogPost, ident=post_id)

    # get form instance with post data
    edit_form = NewPostForm(
        title=existing_post.title,
        subtitle=existing_post.subtitle,
        img_url=existing_post.img_url,
        author=existing_post.author,
        body=existing_post.body
    )

    # Check if post exists
    if not existing_post:
        print("An error occurred. There isn't any post with this id")
        return redirect(url_for('get_all_posts'))

    if edit_form.validate_on_submit():
        existing_post.title = edit_form.title.data
        existing_post.subtitle = edit_form.subtitle.data
        existing_post.author = edit_form.author.data
        existing_post.img_url = edit_form.img_url.data
        existing_post.body = edit_form.body.data

        db.session.commit()

        print('Post updated successfully!')

        return redirect(url_for(endpoint='show_post', post_id=post_id))

    return render_template(template_name_or_list='make-post.html', form=edit_form)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def delete_post(post_id):

    # Find post in database by ID
    post_to_delete = db.session.get(entity=BlogPost, ident=post_id)

    # Check if post exists
    if not post_to_delete:
        print("An error occurred. There isn't any post with this id")
        return redirect(url_for('get_all_posts'))

    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        print("post deleted successfully")
        return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
