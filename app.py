"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def list_users():
    """Lists users and show add form."""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/", methods=["POST"])
def add_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    if request.form['image_url']:
        image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/<int:user_id>")
def show_pet(pet_id):
    """Show info on a single pet."""
    user = User.query.get_or_404(pet_id)
    return render_template("detail.html", user=user)