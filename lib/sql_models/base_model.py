from extensions import db


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    __abstract__ = True

    def mixin_save(self):
        db.session.add(self)
        db.session.commit()

    def mixin_delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        data = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        return data

