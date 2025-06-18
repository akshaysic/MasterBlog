from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "blog_data.json"


def load_posts():
    """
    Load blog posts from the JSON data file.

    Returns:
        list: A list of blog post dictionaries.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_posts(posts):
    """
    Save the list of blog posts to the JSON data file.

    Args:
        posts (list): A list of blog post dictionaries to save.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    """
    Render the homepage with a list of all blog posts.

    Returns:
        str: Rendered HTML template for the homepage.
    """
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post via form submission.

    Returns:
        str: Redirect to homepage or render add post form.
    """
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            "id": max([p["id"] for p in posts], default=0) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template("add.html")


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """
    Edit an existing blog post based on its ID.

    Args:
        post_id (int): The ID of the blog post to edit.

    Returns:
        str: Redirect to homepage or render edit form.
    """
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template("edit.html", post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete a blog post based on its ID.

    Args:
        post_id (int): The ID of the blog post to delete.

    Returns:
        str: Redirect to homepage after deletion.
    """
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
