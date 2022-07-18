from ast import Delete
from crypt import methods
from flask import Flask, render_template, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import User, connect_db, db, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home():

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():

    session.pop("username")
    return redirect("/")


@app.route("/users/<username>")
def details(username):

    if username != session['username'] or "username" not in session:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/details.html", user=user, form=form)


@app.route("/secret/<username>")
def secret(username):

    if username != session['username'] or "username" not in session:
        raise Unauthorized()
    else:
        return render_template("users/secret.html")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if username != session['username'] or "username" not in session:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/")

#####################Feedback routes#################################


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    if username != session['username'] or "username" not in session:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/add.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if feedback.username != session['username'] or "username" not in session:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if feedback.username != session['username'] or "username" not in session:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
