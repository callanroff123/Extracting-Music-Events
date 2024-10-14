import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post


# If we want to test things in a python shell (ex: DB stuff), we can execute "flask shell"
# The below will already be set for us! We can immediately start horsing around
@app.shell_context_processor
def make_shell_context():
    return(
        {"sa": sa, "so": so, "db": db, "User": User, "Post": Post}
    )