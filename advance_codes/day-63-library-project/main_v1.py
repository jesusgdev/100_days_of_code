from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
all_books = []

@app.route('/')
def home():
    if len(all_books) > 0:
        return render_template(template_name_or_list="index.html", books=all_books)
    return render_template(template_name_or_list="index.html")

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':

        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        rating = request.form.get('rating')

        book_entry = {
            "title": book_name,
            "author": book_author,
            "rating": rating
        }
        file_path = "books.json"

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(
                    file=file_path,
                    mode='r',
                    encoding='utf-8'
            ) as f:
                data = json.load(f)
        else:
            data = []

        data.append(book_entry)
        all_books.append(book_entry)

        with open(
                file=file_path,
                mode='w',
                encoding='utf-8'
        ) as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return redirect(url_for('home'))

    return render_template(template_name_or_list="add.html")

if __name__ == "__main__":
    app.run(debug=True)