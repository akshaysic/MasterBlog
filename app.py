from flask import Flask, render_template, request, redirect, url_for
import json
import os
from data_fetcher import fetch_post_by_id, update_post_in_file

app = Flask(__name__)
DATA_FILE = 'posts.json'

def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_post(post):
    posts = load_posts()
    post['id'] = max([p['id'] for p in posts], default=0) + 1
    posts.append(post)
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

def delete_post(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        save_post(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    delete_post(post_id)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        updated_post = {
            'id': post_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        update_post_in_file(updated_post)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
