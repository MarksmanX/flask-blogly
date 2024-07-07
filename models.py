"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models for user
class User(db.Model):
    """User."""

    __tablename__ = 'users'

    def __repr__(self):
        p = self
        return f"<User Id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url or 'N/A'}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25),
                           nullable=False,
                           unique=True)
    
    last_name = db.Column(db.String(25),
                           nullable=False,
                           unique=True)
    
    image_url = db.Column(db.String,
                          nullable=False,
                          default='static/images/default_user_pic.jpg')
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post."""

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post Id={p.id} Title={p.title} Content={p.content} Created at={p.time} FK={p.user}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=func.now())
    user_code = db.Column(db.Integer,
                          db.ForeignKey('users.id'),
                          nullable=False)
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
