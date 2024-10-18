from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from flask_bootstrap import Bootstrap5
import pandas as pd
from datetime import datetime, timedelta
from app.forms import LoginForm, RegistrationForm, FilterForm
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
    

if __name__ == "__main__":
    app.run(debug = True, port = 5000)