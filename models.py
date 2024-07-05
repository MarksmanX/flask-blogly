"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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


    # @classmethod
    # def todooooooooooooo  