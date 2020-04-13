# start by importing teh test case from Django 
from django.test import TestCase
# next import the 'create_user' helper function that comes with Django
# We can import the user model directly from the models but it is not recommended with django because 
# at some point in the project you may want to change what your user model is and if 
# everything is using the 'get_user_model' function then that is really easy to do so since you can just 
# change it in the settings rather than changing all the references to the user model. 
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
		test creating a user with an email is successful

		To setup the test- 
		1. We are simply going to pass an email address and a password. 
		2. verify that the user has been created. 
		3. verify that the email_id is correct and the pasword is correct.
		"""

        email = "test@pritish.com"
        # does not matter if the password is secure since it will only be created for the sake of test case
        # mdoel is deleted afterwards
        password = "learndjango"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # note that password cannot be checked same as user since password is encrypted.
        # check_passweord is a helper function that comes with the Django user_model.
        # check_password basically returns True if the password is True else return False.
        self.assertTrue(user.check_password(password))

    # run the unit test by using command docker-compose run app sh -c "python manage.py test"
    # the first time we run command it will fail with error - TypeError: create_user() missing 1 required positional argument: 'username'
    # This is because we havent customized the user model and it is still expecting the standard username field that is
    # required for the Django default user model.

    def test_new_user_email_normalized(self):
        """
		test the email for a new user is normalized.
		"""

        email = 'test@PRITISH.COM'

        user = get_user_model().objects.create_user(
            email=email,
            password='test@123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
		test creating user with no email generates an error
		"""

        # the with basically ensure that whatever we run within the scope must raise a valueError.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="test123")

    def test_create_super_user(self):
        """
		test creating a new super user
		"""

        user = get_user_model().objects.create_superuser(
            'test@pritish.com',
            'test123'
        )

        # is_superuser is not a part of the User model but is included as a part of PermissionMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
