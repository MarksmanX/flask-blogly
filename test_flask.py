import unittest

from app import app
from models import User, db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testdb'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(unittest.TestCase):
    """Test views for Users."""

    def setUp(self):
        """Add sample pet."""

        self.app_context = app.app_context()
        self.app_context.push()
        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="static/images/default_user_pic.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        self.app_context.pop()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/{self.user_id}">Test User</a>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Test User Details</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "User", "last_name": "2", "image_url": "static/images/default_user_pic.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>User 2 Details</h1>", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(">User 2</a>", html)