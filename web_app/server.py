from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.fields import DateField, SelectMultipleField, SearchField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import pandas as pd
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = "xxxx"
bootstrap = Bootstrap5(app)
df = pd.read_csv("../output/music_events.csv")


class FilterForm(FlaskForm):
    start_date = DateField(
        label = "From: ", 
        format = "%Y-%m-%d"
    )
    end_date = DateField(
        label = "To: ", 
        format = "%Y-%m-%d"
    )
    venue_filter = SelectMultipleField(
        label = "Filter Venues: ",
        choices = list(df["Venue"].unique())
    )
    search_field = StringField(
        label = "Keyword: "
    )
    submit = SubmitField("OK")


@app.route("/")
def home():
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
    data_refined = df_refined.to_dict("records")
    return(render_template(
        "gigs.html",
        data = data_refined,
        form = form
    ))


@app.route('/refresh_filters', methods = ["GET", "POST"])
def refresh_filters():
    return(redirect(url_for('gigs')))
    

if __name__ == "__main__":
    app.run(debug = True, port = 5000)