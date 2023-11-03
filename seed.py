from flask import Flask
from models import User, db, connect_db
from app import app


with app.app_context():
    # Create all tables
    # assumes the database "blogly" exists... if not, create it manually
    db.drop_all()
    db.create_all()



    User.query.delete()

    # Add a bunch of users
    u1 = User(first_name="Karl", last_name="Haakonsen",image_url="https://pbs.twimg.com/profile_images/638032919148146688/0piPz3z7_400x400.jpg")
    u2 = User(first_name="Frank", last_name="Furter", image_url="https://static.wikia.nocookie.net/villains/images/5/5f/SweetTransvestite.jpg")
    u3 = User(first_name="Martin", last_name="Brody", image_url="https://static.wikia.nocookie.net/jaws/images/3/39/Brody.jpg")
    u4 = User(first_name="John", last_name="Ballen", image_url="https://mrballen.foundation/wp-content/uploads/2023/05/2023-05-08-15.11.16-1-682x1024.jpg")

    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()