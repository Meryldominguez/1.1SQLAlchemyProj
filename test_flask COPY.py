from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Testuser",last_name="Usertest", image_url="www.lorempicsum.com/100")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)

    def test_list_users(self):
        with app.test_client() as client:

            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testuser Usertest', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Testuser Usertest</h1>', html)

    def test_view_new_user(self):
        with app.test_client() as client:
            resp= client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>Add User</h2>", html)

    def test_add_new_user(self):
        with app.test_client() as client:
            formdata = {'first_name':"Testuser2" , 'last_name':"Usertest2" , 'image_url': "www.lorempicsum.com/300"}
            resp = client.post("/users/new", data=formdata, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testuser2 Usertest2", html)


            # formdata2 = {'first_name':"Testuser3" , 'last_name':"Usertest3", 'image_url':""}
            # resp2 = client.post("/users/new", data=formdata2, follow_redirects=True)
            # html2 = resp2.get_data(as_text=True)
            # self.assertEqual(resp.status_code, 200)
            # self.assertIn("Testuser3 Usertest3", html2)
            # response
            # self.assertIn("https://picsum.photos/200", html2)


