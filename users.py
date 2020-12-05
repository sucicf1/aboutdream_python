from settings import *
from passlib.hash import sha256_crypt
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)
import json
from sqlalchemy.orm import relationship, mapper

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        if not token:
            token=''
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data["id"])
        return user 

    def verify_password(self, _password):
        if sha256_crypt.verify(_password, self.password_hash):
            return True
        return False

    def add_user(_username, _password):
        new_user = User(
            username=_username,
            password_hash=sha256_crypt.hash(bytes(_password, "utf-8")),
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user