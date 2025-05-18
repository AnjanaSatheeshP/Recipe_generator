from flask import Flask, render_template, request, session, redirect, url_for, flash
import json
from recipe_model import generate_recipe

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  

def load_users():
    """Load users from users.json or return an empty dict."""
    try:
        with open('users.json') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('input'))  # Redirect to input page after login

    if request.method == "POST":
        users = load_users()
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email] == password:
            session['username'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('input'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

def save_user(email, password):
    users = load_users()
    users[email] = password
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        users = load_users()

        if email in users:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        save_user(email, password)
        flash('Signup successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/input')
def input():
    if 'username' not in session:
        flash('Please log in to access the recipe generator.', 'warning')
        return redirect(url_for('login'))
    return render_template('input.html')

@app.route('/generate', methods=["POST"])
def generate():
    if 'username' not in session:
        return redirect(url_for('login'))

    ingredients = request.form.get('ingredients')
    raw_recipe = generate_recipe(ingredients)

    formatted_recipe = (
        raw_recipe.replace("title:", "<b>Title:</b><br>")
                  .replace("ingredients:", "<br><br><b>Ingredients:</b><br>")
                  .replace("directions:", "<br><br><b>Directions:</b><br>")
    )

    return render_template('result.html', ingredients=ingredients, recipe=formatted_recipe)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
