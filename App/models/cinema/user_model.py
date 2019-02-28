from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.models import BaseModel


class CinemaUser(BaseModel):
    c_name = db.Column(db.String(32), unique=True)
    _c_password = db.Column(db.String(256))

    @property
    def c_password(self):
        raise Exception("can't access")

    @c_password.setter
    def c_password(self, password):
        self._c_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._c_password, password)


class Permission(BaseModel):
    __tablename__ = "c_u_permission"
    p_name = db.Column(db.String(64), unique=True)


class CinemaPermission(BaseModel):
    u_permission_id = db.Column(db.Integer, db.ForeignKey(Permission.id))
    u_user_id = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))