"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    return redirect("/users")

@app.route("/users")
def list_users():
    """Lists users and show add form."""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET","POST"])
def add_user():
    """Add user and redirect to list."""
    if request.method == "GET":
        return render_template("new_user.html")
    elif request.method=="POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if not request.form['image_url']:
            image_url = "https://picsum.photos/200"
        else:
            image_url = request.form['image_url']

        user = User(first_name=first_name.title(), last_name=last_name.title(), image_url=image_url)
        db.session.add(user)
        db.session.commit()

        return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET","POST"])
def show_user_edit(user_id):
    """view and edit info on a single user."""
    if request.method =="GET":
        user = User.query.get_or_404(user_id)
        return render_template("edit.html", user=user)
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if not request.form['image_url']:
            image_url = "https://picsum.photos/200"
        else:
            image_url = request.form['image_url']
        user = User.query.get_or_404(user_id)

        user.first_name=first_name.title()
        user.last_name=last_name.title()
        user.image_url=image_url
        db.session.add(user)
        db.session.commit()
        response.status_code = 200
        return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")