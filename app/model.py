from werkzeug.security import check_password_hash, generate_password_hash
import pymongo

def encrypt_passowrd(password):
    return generate_password_hash(password)

class User():

    def __init__(self, username):
        self.username = username
        #self.email = None
        self.db = pymongo.MongoClient("localhost", 27017)['blog'].users

    def new_user(self, email, password):
        collection = {
            '_id': self.username,
            'email': email,
            'password': encrypt_passowrd(password)
        }
        self.db.insert(collection)
            

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
