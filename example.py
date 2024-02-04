from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json
from uuid import uuid4
import sys


app = Flask(__name__)
app.secret_key = "secret_key"
@app.route('/')
def index():
    url_for('users')
    url_for('new_user')
    url_for('create_user')
    return 'Hello, World!'


@app.get('/users/')
def users():
    messages = get_flashed_messages(with_categories=True)
    with open('users.json', 'r') as f:
        users = json.loads(f.read())
    return render_template(
        'index.html',
        users=users,
        messages=messages
    )


@app.get('/users/new/')
def new_user():
    user = {
        'nickname': '',
        'email': ''
    }
    errors = {}
    return render_template(
        'users/new.html',
        users=user,
        errors=errors,
    )

@app.post('/users/')
def create_user():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors
        ), 422
    user['id'] = str(uuid4())
    with open('users.json', 'r') as f:
        old_data = json.loads(f.read())
    new_data = []
    new_data.append(user)
    with open('users.json', 'w') as f:
        f.write(json.dumps(old_data + new_data))
    flash('User created success', 'success')
    return redirect(url_for('users'), code=302)


def validate(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    elif len(user['nickname']) <= 4:
        errors['nickname'] = "Nickname must be greater than 4 characters"
    elif not user['email']:
        errors['email'] = "Can't be blank"
    elif not '@' in user['email']:
        errors['email'] = "Must be '@' symbol"
    return errors