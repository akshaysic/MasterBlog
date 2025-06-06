import json
import os

DATA_FILE = 'posts.json'

def fetch_post_by_id(post_id):
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        posts = json.load(f)
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

def update_post_in_file(updated_post):
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r') as f:
        posts = json.load(f)
    for i, post in enumerate(posts):
        if post['id'] == updated_post['id']:
            posts[i] = updated_post
            break
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=2)
