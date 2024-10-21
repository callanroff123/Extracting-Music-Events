from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_login import current_user
import sqlalchemy as sa
import pandas as pd
from datetime import datetime
from app import db
from app.models import User


try:
    df = pd.read_csv("../output/music_events.csv")
    df = df[pd.to_datetime(df["Date"]) >= pd.to_datetime(datetime.now().date())]
except:
    df = pd.read_csv("./output/music_events.csv")
    df = df[pd.to_datetime(df["Date"]) >= pd.to_datetime(datetime.now().date())]


class LoginForm(FlaskForm):

    username = StringField(label = "Username", validators = [DataRequired()])
    password = PasswordField(label = "Password", validators = [DataRequired()])
    remember_me = BooleanField(label = "Remember Me")
    submit = SubmitField(label = "Sign In")


class RegistrationForm(FlaskForm):

    username = StringField(label = "Username", validators = [DataRequired()])
    email = StringField(label = "Email", validators = [DataRequired(), Email()])
    password = PasswordField(label = "Password", validators = [DataRequired()])
    password_confirm = PasswordField(
        label = "Confirm Password", 
        validators = [DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # When we add a method of the structure "validate_<field_name>", FlaskForm automatically takes those as custom validators
    # Automatically invoked in addition to the 'stock' validators called (ex: DataRequired())
    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(
                User.username == username.data
            )
        )
        if user is not None:
            raise ValidationError("Please use a different username.")
        
    def validate_email(self, email):
        user = db.session.scalar(
            sa.select(User).where(
                User.email == email.data
            )
        )
        if user is not None:
            raise ValidationError("Please use a different email address.")
        

class EditProfileForm(FlaskForm):

    # This base method will initalise a user's 'original username'
    # Covers the automfilling of the original username into the "username" field??
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.username.render_kw = {"placeholder": original_username}

    username = StringField(label = "Username", validators = [DataRequired()])
    about_me = TextAreaField(label = "About Me", validators = [Length(min = 0, max = 140)])
    submit = SubmitField(label = "Submit")

    # Ensure the user's updated username is not already taken
    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(
                User.username == username.data
            )
        )
        if (user is not None) and (user != current_user):
            raise ValidationError("Please use a different username.")
        

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