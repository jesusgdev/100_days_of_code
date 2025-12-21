from flask import Flask, render_template, request
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import requests
import random
import json
import os


app = Flask(__name__)

# Generate random dates with the format "%B %d, %Y" -> "November 01, 2025"
dates = [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d") for d in range(30)]
dates.sort(reverse=True)
dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y") for date in dates]


def get_fake_posts():
    response = requests.get("https://dummyjson.com/posts")
    posts_response = response.json()["posts"]

    adapted = []
    for p in posts_response:
        adapted.append({
            "id": p["id"],
            "author": "Jesus Garcia",
            "title": p["title"],
            "subtitle": p["title"] + " — A deeper look",
            "body": p["body"],
            "image_url": f"https://picsum.photos/1200/600?random=1",
            "date": dates[p['id'] - 1],
        })
    return adapted

posts = get_fake_posts()

with open(file="posts.json", mode="w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    # Obtener página actual desde query param (default: 1)
    page = request.args.get('page', 1, type=int)

    all_posts = get_fake_posts()

    # Configuración de paginación
    posts_per_page = 5
    start_idx = (page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page

    # Posts de la página actual
    actual_posts = all_posts[start_idx:end_idx]

    # Calcular si hay página siguiente/anterior
    has_prev = page > 1
    has_next = end_idx < len(all_posts)

    return render_template(
        'index.html',
        posts=actual_posts,
        page=page,  # ✅ Página actual
        has_prev=has_prev,  # ✅ ¿Hay página anterior?
        has_next=has_next,  # ✅ ¿Hay página siguiente?
        prev_page=page - 1,  # ✅ Número de página anterior
        next_page=page + 1  # ✅ Número de página siguiente
    )

@app.route('/post/<int:post_id>')
def post(post_id):
    all_posts = get_fake_posts()
    post_data = next((p for p in all_posts if p['id'] == post_id), None)

    if not post_data:
        return "Post not found", 404

    return render_template('post.html', post=post_data)

@app.route('/about')
def about():
    return render_template('about.html')

load_dotenv()

# Configuration
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email data
recipient = MY_EMAIL
subject = "Blog Form Message"


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        body_msg = (f"Name: {username}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Message: {message}")

        # Create Message
        msg = MIMEText(body_msg)
        msg['Subject'] = subject
        msg['From'] = MY_EMAIL
        msg['To'] = recipient

        # Send Email Process
        try:
            # Connect to server
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls() # Activate TLS Security

            # Login
            server.login(MY_EMAIL, MY_PASSWORD)

            # Send Email
            server.send_message(msg)

            # Close connection
            server.quit()

            print("✅ Email sent successfully!")

        except Exception as e:
            print(f"❌ Error to send email: {e}")

        # print(f"{username}\n"
        #       f"{email}\n"
        #       f"{phone}\n"
        #       f"{message}")

        return render_template('contact.html')
    else:
        return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)


