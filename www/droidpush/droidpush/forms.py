from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import ValidationError
from flaskext.wtf.html5 import EmailField
from flaskext.mongokit import MongoKit
from droidpush import app

db = MongoKit(app)

def unique_email(form, field):
    # Check to see if this email already exists
    user_search = db.users.find_one({"email": field.data})
    if user_search != None:
        raise ValidationError('Looks like this email address is already registered')

class RegistrationForm(Form):
    email = EmailField('Email Address', [
        validators.Required(),
    	validators.Length(min=6, max=100),
    	validators.Email(),
        unique_email
    ])
    password = PasswordField('Password', [
    	validators.Required(),
        validators.Length(min=6, max=100),
    	])
    terms = BooleanField('Terms and conditions', [
    	validators.Required()
    ])