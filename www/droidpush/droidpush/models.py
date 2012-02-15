from flaskext.mongokit import MongoKit, Document
from datetime import datetime


class User(Document):
    __collection__ = 'users'
    __database__ = 'droidpush'

    structure = {
        'email': unicode,
        'password': unicode,
        'created': datetime,
        'status': int
    }
    required_fields = ['email', 'password', 'created']
    default_values = {'created': datetime.utcnow, 'status': 1}
    use_dot_notation = True