from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import ValidationError
from flaskext.wtf.html5 import EmailField
from flaskext.mongokit import MongoKit
from droidpush import app
from droidpush.models import check_password, User

db = MongoKit(app)

def unique_email(form, field):
    # Check to see if this email already exists
    user_search = db.users.find_one({"email": field.data})
    if user_search != None:
        raise ValidationError('Looks like this email address is already registered')

class RegistrationForm(Form):
    email = EmailField('Email Address', [
        validators.Required(),
    	validators.Length(min=6, max=200),
    	validators.Email(),
        unique_email
    ])
    password = PasswordField('Password', [
    	validators.Required(),
        validators.Length(min=6, max=200),
    ])
    terms = BooleanField('Terms and conditions', [
    	validators.Required()
    ])

class LoginForm(Form):
    email = EmailField('Email Address', [
        validators.Required(),
        validators.Length(min=6, max=200),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=200),
    ])
    remember = BooleanField('Remember me', [])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def get_user(self):
        return self.user

    def validate(self):
        # for login validation we need to have a common error message for the
        # different type of login errors, so people can lot game the system and
        # work out what email exist
        error_message = 'Login failed. Perhaps check your email or password'

        # regular validation
        rv = Form.validate(self)
        if not rv:
            return False

        # check the user model to see if the login credentials are valid
        user_model = User()
        if user_model.validate_login(self.email.data,self.password.data):
            # login credentials all good, set the user (which has now been
            # populated with the user details)
            self.user = user_model
            return True
        else:
            self.email.errors.append(error_message)
            return False