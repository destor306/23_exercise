from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_greet(self):
        user = User(first_name="Jason", last_name="Yoo")
        self.assertEqual(
            user.greet(), f"I'm {user.first_name} {user.last_name}")

    def test_get_ful_name(self):
        user = User(first_name="Jason", last_name="Yoo")

        self.assertEqual(user.get_full_name(),
                         f"{user.first_name} {user.last_name}")

    def test_list_by_lastname(self):
        user = User(first_name="Jason", last_name="Yoo")
        user1 = User(first_name="Jayson", last_name="ABC")
        db.session.add(user)
        db.session.add(user1)
        db.session.commit()

        list = User.list_by_lastname()
        self.assertEqual(list, [user1, user])
