"""File containing SQLAlchemy model classes"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
#from app import app


# This is the connection to the database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##################################################################

# Model definitions

"""Models for Blogly."""

class User(db.Model):
    """class for SQLAlchemy model User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    #posts = db.relationship(Post)

    def __repr__(self):
        e = self
        return f"<User {e.id} {e.first_name} {e.last_name}, {e.image_url}>"
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    
           
    
class Post(db.Model):
    """class for SQLAlchemy model Post"""

    __tablename__ = "posts"

    now = datetime.now()

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=now, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    #user = db.relationship(User)                    

    user = db.relationship(User, backref = 'posts')                    

    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.content}, {p.created_at}, {p.userid}>"
    @property
    def pretty_date(self):
        """Return formatted datetime."""
        p = self
        return p.created_at.strftime("%b %d, %Y, %-I:%M %p")
    
    @property
    def has_posts(self):
        num_posts = self.Query.filter_by(userid=self.userid).count()
        print(f"user {self.full_name}, num_posts = {num_posts}")
        return 'yes' if num_posts > 0 else 'no'
        



####### Helper functions

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    print("executing if __name__ == __main__")
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from app import app
    connect_db(app)

    db.drop_all()
    db.create_all()