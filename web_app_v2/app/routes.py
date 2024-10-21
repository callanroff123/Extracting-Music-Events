from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from flask_bootstrap import Bootstrap5
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.forms import LoginForm, RegistrationForm, FilterForm, EditProfileForm
from app.models import User, Post, Event
from app import app, db, login


try:
    df = pd.read_csv("../output/music_events.csv")
    df = df[pd.to_datetime(df["Date"]) >= pd.to_datetime(datetime.now().date())]
except:
    df = pd.read_csv("./output/music_events.csv")
    df = df[pd.to_datetime(df["Date"]) >= pd.to_datetime(datetime.now().date())]


@app.route("/")
@app.route("/index")
def index():
    return(render_template(
        "index.html"
    ))


@app.route("/gigs", methods = ["GET", "POST"])
def gigs():
    form = FilterForm()
    if form.start_date.data is None:
        df_refined = df.copy()
    else:
        df_refined = df[
            (pd.to_datetime(df["Date"]) >= pd.to_datetime(form.start_date.data))
        ].reset_index(drop = True)
    if form.end_date.data is None:
        pass
    else:
        df_refined = df_refined[
            (pd.to_datetime(df["Date"]) <= pd.to_datetime(form.end_date.data))
        ].reset_index(drop = True)
    if form.venue_filter.data is None or [x.replace(" ", "") for x in list(form.venue_filter.data)] in [[], [""]]:
        pass
    else:
        df_refined = df_refined[
            (df["Venue"].isin(list(form.venue_filter.data)))
        ].reset_index(drop = True)
    if form.search_field.data is None or [x.replace(" ", "") for x in list(form.search_field.data)] in [[], [""]]:
        pass
    else:
        df_refined = df_refined[
            df_refined["Title"].str.lower().str.contains(form.search_field.data.lower()) |
            df_refined["Venue"].str.lower().str.contains(form.search_field.data.lower())
        ]
    if len(df_refined) < len(df):
        flash("Filter applied!")
    data_refined = df_refined.to_dict("records")
    return(render_template(
        "gigs.html",
        data = data_refined,
        form = form
    ))


@app.route('/refresh_filters', methods = ["GET", "POST"])
def refresh_filters():
    return(redirect(url_for('gigs')))


@app.route("/profile/<username>")
def profile(username):
    user = db.first_or_404(
        sa.select(User).where(
            User.username == username
        )
    )
    posts_query = user.posts.select()
    posts = db.session.scalars(posts_query).all()
    # Sanity checks
    print(user)
    print(current_user)
    for post in posts:
        print(post.body)
        print(post.timestamp)
        print(post.user_id)
    # End of sanity checks
    return(render_template(
        "profile.html",
        user = user,
        posts = posts
    ))

@app.route("/edit_profile", methods = ["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(original_username = current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved!")
        return(redirect(url_for("profile", username = current_user.username)))
    # For the initial request
    # When the form is being accessed initially, pre-fill the fields with default/existing user data
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return(render_template(
        "edit_profile.html",
        title = "EditProfile",
        form = form
    ))


@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for("index")))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.first_or_404(
            sa.select(User).where(
                User.username == form.username.data
            )
        )
        if (user is None) or (not check_password_hash(user.password_hash, form.password.data)):
            flash("Invalid login credentials")
            return(redirect(url_for("login")))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get("next")
        if (not next_page) or (urlsplit(next_page).netloc != ""):
            next_page = url_for("index")
        return(redirect(next_page))
    return(render_template(
        "login.html",
        title = "Sign In",
        form = form
    ))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return(redirect(url_for("index")))


@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Cannot register a new user while logged in.")
        return(redirect(url_for("index")))
    form  = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data
        )
        new_user.set_password(password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Welcome to the community, {form.username.data}!")
        return(redirect(url_for("login")))
    return(render_template(
        "register.html",
        form = form,
        title = "Register"
    ))
    

if __name__ == "__main__":
    app.run(debug = True, port = 5000)