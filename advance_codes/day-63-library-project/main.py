from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
new_rating = 0

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # ✅ Read from the database each time
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()

    # Pass data to the template
    return render_template("index.html", books=all_books)

@app.route('/delete/<int:id>')
def delete(id):
    # Search the book by ID
    book_to_delete = db.session.execute(
        db.select(Book).where(Book.id == id)
    ).scalar()

    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route(rule="/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        rating = request.form.get('rating')

        # ✅ Save to the database
        # No need for app_context inside routes
        new_book = Book(title=book_name, author=book_author, rating=float(rating))
        db.session.add(new_book)
        db.session.commit()

        # ✅ Redirect to home (home() will read the updated book list)
        return redirect(url_for('home'))

    return render_template("add.html")

@app.route(rule="/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    # Search the book by ID
    book_to_update = db.session.execute(
        db.select(Book).where(Book.id == id)
    ).scalar()

    # Check if it exist
    if not book_to_update:
        return "<p>Book not found</p>", 404

    # If it is POST, update
    if request.method == 'POST':

        # Get new rating of the form
        new_rating = request.form.get('rating')

        # Update the rating
        book_to_update.rating = float(new_rating)

        # Save changes
        db.session.commit()

        # Redirect to home
        return redirect(url_for('home'))

    # If it is GET, show the form
    return render_template(template_name_or_list="edit.html", book=book_to_update)


if __name__ == "__main__":
    app.run(debug=True)