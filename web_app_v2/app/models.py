from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import db, login


class User(UserMixin, db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index = True, unique = True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index = True, unique = True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[str]] = so.mapped_column(
        default = lambda: datetime.now(timezone.utc)
    )

    # Specifying this relationship allows joins to the PK field (ID) to the related FK field (user_id) in another table 
    # WriteOnly Type -> 'posts' field contains Post objects inside
    # ex: user.posts => [<Post dcdcdc>, <Post vvvtvt>]
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates = "author")
    events: so.WriteOnlyMapped['Event'] = so.relationship(back_populates = "organiser")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return(check_password_hash(self.password_hash, password))
    
    # Generate a 'Gravatar' icon for a newly registered user, given their email
    # "d" argument in URL determines what image (identicon) Gravatar provides with users which do not have an avatar with Gravatar
    # ".encode("utf-8") encodes the string as bytes, since MD5 support requires it"
    # We then pass the bytes to a hash function ('hexdigest')
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return(f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}')
    
    def __repr__(self):
        return(f"<User {self.username}>")
    

# Invoked whenever 'flask_login.current_user' is called in the application
@login.user_loader
def load_user(id):
    return(db.session.get(User, int(id)))


class Post(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    body: so.Mapped[str] = so.mapped_column(sa.String(300))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index = True,
        default = lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index = True)

    # "so.relationship()" allows us to join the FK field to the PK in another table (and vice-versa) I THINK?!
    # This is not an actual field in the 'Post' table; we still just have id, body, timestamp and user_id
    # We need to specify who the user is when we create a Post instance
    author: so.Mapped[User] = so.relationship(back_populates = "posts")

    def __repr__(self):
        return(f"<Post {self.body}>")


class Event(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    event_name: so.Mapped[str] = so.mapped_column(sa.String(300), index = True)
    event_link: so.Mapped[str] = so.mapped_column(sa.String(300))
    event_date: so.Mapped[str] = so.mapped_column(sa.String(100), index = True)
    event_venue: so.Mapped[str] = so.mapped_column(sa.String(100), index = True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index = True,
        default = lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index = True)

    # A new relationship defined with the User table..
    organiser: so.Mapped[User] = so.relationship(back_populates = "events")

    def __repr__(self):
        return(f"<Event {self.event_name}>")

