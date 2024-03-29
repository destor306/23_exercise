"""Seed file to make sample data for pets db"""

from models import User, Post, PostTag, Tag, db
from app import app


# Create all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
Post.query.delete()
User.query.delete()

# add User
bob = User(first_name="Bob", last_name="Sponge")
jason = User(first_name="Jason", last_name="Yoo")
ace = User(first_name="Ace", last_name="YOU")

db.session.add_all([bob, jason, ace])
db.session.commit()

# add tags
tag1 = Tag(name="Funny")
tag2 = Tag(name="Tech")
tag3 = Tag(name="Car")

# add posts
post1 = Post(title="First", content="This is firstPost", user_id=bob.id)
post2 = Post(title="Second", content="This is 2", user_id=jason.id)
post3 = Post(title="Third", content="This is 3", user_id=ace.id)

# Commit--otherwise, this never gets saved!
db.session.add_all([post1, post2, post3])
db.session.commit()

# Associate Tags with posts
post1.tags.extend([tag1, tag2])
post2.tags.append(tag3)
post3.tags.append(tag1)

db.session.commit()
