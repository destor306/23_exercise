from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()
        user = User(first_name="Test123", last_name="Yoo")
        db.session.add(user)
        db.session.commit()

        # post = Post(title="This is test",
        #             content="This is just test", user_id=user.id)
        # db.session.add(post)
        # db.session.commit()

        self.user_id = user.id
        self.user = user

        # self.post_id = post.id
        # self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test123 Yoo', html)

    def test_create_user(self):
        with app.test_client() as client:
            form_data = {
                'first_name': 'Test132',
                'last_name': 'Test2',
                'imageurl': 'test.jpg'
            }
            resp = client.post("/users/new", data=form_data,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test132 Test2", html)

    def test_show_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>{self.user.full_name}</h1>", html)

    def test_edit_user(self):
        with app.test_client() as client:
            # Create a user to edit
            user = User(first_name="John", last_name="Doe",
                        image_url="test.jpg")
            db.session.add(user)
            db.session.commit()

            form_data = {
                'first_name': 'UpdatedFirst',
                'last_name': 'UpdatedLast',
                'image_url': 'updated.jpg'
            }

            # Send a POST request to edit the user
            resp = client.post(
                f"/users/{user.id}/edit", data=form_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Assert that the user was updated successfully
            self.assertEqual(resp.status_code, 200)
            self.assertIn('UpdatedFirst UpdatedLast', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

        # Create a user to delete
        user = User(first_name="John", last_name="Doe", image_url="test.jpg")
        db.session.add(user)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        # Assert that the user was deleted successfully
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('John Doe', html)
        # self.assertNotIn(b'Test Post', response.data)

    # def test_post(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/posts/{self.post_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn(f"<h1>{self.post.title}</h1>", html)
