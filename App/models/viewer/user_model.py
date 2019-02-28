from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.models import BaseModel


PERMISSION_READ = 1
PERMISSION_WRITE = 2


class ViewerUser(BaseModel):
    v_phone = db.Column(db.String(32), unique=True)
    _v_password = db.Column(db.String(256))
    v_permission = db.Column(db.Integer, default=PERMISSION_READ & PERMISSION_WRITE)

    @property
    def v_password(self):
        raise Exception("can't access")

    @v_password.setter
    def v_password(self, password):
        self._v_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._v_password, password)

    def check_permission(self, permission):
        return self.v_permission & permission == permission
