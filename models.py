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

    # direct navigation: emp -> PostTag & back
    post_tags = db.relationship('PostTag',
                                  backref='post')

    # direct navigation: post -> tag & back
    tags = db.relationship('Tag',
                               secondary='post_tag',
                               backref='posts')           

    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.content}, {p.created_at}, {p.userid}>"
    @property
    def pretty_date(self):
        """Return formatted datetime."""
        p = self
        return p.created_at.strftime("%b %d, %Y, %-I:%M %p")
    
           

class Tag(db.Model):
    """ Class for Post "Tag" """
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    name = db.Column(db.Text, nullable=False)

 # direct navigation: proj -> employeeproject & back
    post_Tag = db.relationship('PostTag',
                                  backref='tags', cascade="all, delete")

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"
                 

class PostTag(db.Model):
    """Class for many-to-many link table between posts and tags"""
    __tablename__ = "post_tag"
    
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id =  db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)



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