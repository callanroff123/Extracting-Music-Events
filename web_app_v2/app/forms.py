from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
import sqlalchemy as sa
from app import db
from app.models import User


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