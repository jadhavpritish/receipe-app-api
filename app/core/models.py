from django.db import models
# import modules needed to extend the Django user model whilst making use of some of 
# the features that come with the djnago user model out of the box. 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# We can now create our user manager class. 
# Manager class is the class that provides the helper functions for creating a user
# or creating a super user.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        # The last argument basically says that take any of the extra
        # functions that are passed in when you call the create_user
        # and pass them into extra_fields so that we can then just
        # add any additional fields that we craete without user_model.
        # It is not required but it just makes our function a little more
        # flexible because everytime we add a new field to our user it means
        # we dont have to add them in here. We can just add them ad-hoc as we add them to
        # our model.

        """
		creates and saves a new user

		normalize_email is a helper function that comes with BaseUserManager
		"""

        # check if email is valid
        if not email:
            raise ValueError("users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        # The way that the management commands work is you can access
        # the model that the manager is for by just typing self.model.
        # This is effectively the same as creating a new user model
        # and assigning it to the user variable.
        user.set_password(password)
        user.save(using=self.db)

        # So when you call the create_user funtion it creates a new user model and
        # sets the password, saves the model and return the user model
        return user

    def create_superuser(self, email, password):
        """
		Creates and saves a new superuser
		"""

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
	custom user model that supports using email address instead of username
	"""

    # define fields of our database model.
    # unique=True ensure that there is only one user per email_id
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # creates a new user manager for our object
    objects = UserManager()

    # by default the username field is username and we are customizing that to
    # email so that we can use an email address
    USERNAME_FIELD = 'email'
