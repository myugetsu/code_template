import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from flask_login import UserMixin
from flask import current_app, url_for
from app import db, login
import base64
from datetime import datetime, timedelta
import os
from app.utils.auth_token import generate_token


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(128), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # 'last_seen': self.last_seen.isoformat() + 'Z',
            "_links": {"self": url_for("api.get_user", id=self.id)},
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ["username", "email", "about_me"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def check_user_exist(self, data):
        user = self.query.filter(
            (User.username == data["username"]) | (User.email == data["email"])
        ).first()
        if user:
            return True
        else:
            return False

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        # self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token = generate_token(self.id)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
