from werkzeug.security import check_password_hash, generate_password_hash
import pymongo

def encrypt_passowrd(password):
    return generate_password_hash(password)

class User():

    def __init__(self, username, email, password, about_me):
        self.username = username
        self.email = email
        self.password = password
        self.about_me = about_me
        self.db = pymongo.MongoClient("localhost", 27017)['blog'].users

    def new_user(self):
        collection = {
            'username': self.username,
            'email': self.email,
            'password': encrypt_passowrd(self.password),
            'about_me': self.about_me

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


class Temp():

    def __init__(self, id, username, email, password, about_me):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password_hash = password
        about_me = about_me

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
