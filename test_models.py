from unittest import TestCase

from app import app
from models import db, User
# from flask_sqlalchemy import SQLAlchemy

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()
        invalid = User( last_name="Keeney", image_url="www.lorempicsum.com/100")

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        valid = User(first_name="Marie", last_name="Keeney", image_url="www.lorempicsum.com/100")

        self.assertEqual(valid.get_full_name(), "Marie Keeney")
        self.assertEqual(valid.get_full_name(), valid.first_name+" "+valid.last_name)

    # def test_bad_user(self):
    #     invalid = User( last_name="Keeney", image_url="www.lorempicsum.com/100")
        
    #     with self.assertRaises(SQLAlchemy.exc.IntegrityError, invalid):
    #         db.session.add(invalid)
    #         db.session.commit()
