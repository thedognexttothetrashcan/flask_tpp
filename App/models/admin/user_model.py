from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.models import BaseModel


class AdminUser(BaseModel):
    a_name = db.Column(db.String(32), unique=True)
    _a_password = db.Column(db.String(256))
    is_super = db.Column(db.Boolean, default=False)

    @property
    def a_password(self):
        raise Exception("can't access")

    @a_password.setter
    def a_password(self, password):
        self._a_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._a_password, password)


class Permission(BaseModel):
    p_name = db.Column(db.String(64), unique=True)


class UserPermission(BaseModel):
    u_permission_id = db.Column(db.Integer, db.ForeignKey(Permission.id))
    u_user_id = db.Column(db.Integer, db.ForeignKey(AdminUser.id))