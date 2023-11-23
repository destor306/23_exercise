from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)

    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=False)

    image_url = db.Column(db.String(50),
                          nullable=True,
                          default='Ace.jpg')

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def list_by_lastname(cls):
        """Return list of name by last name"""
        return cls.query.order_by(cls.last_name).all()

    @classmethod
    def list_by_fisrtname(cls):
        """Return list of name by first name"""
        return cls.query.order_by(cls.first_name).all()

    def __repr__(self):
        p = self
        return f"<User id={p.id} name={p.first_name} {p.last_name}>"

    def greet(self):
        return f"I'm {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)

    # Define the foreign key relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
