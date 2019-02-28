from App.ext import db


class BaseModelNoPrimary(db.Model):
    __abstract__ = True

    def save(self):
        try:

            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def delete(self):
        try:

            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True



class BaseModel(BaseModelNoPrimary):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    is_delete = db.Column(db.Boolean, default=False)

    def delete_logic(self):
        self.is_delete = True

        try:

            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True