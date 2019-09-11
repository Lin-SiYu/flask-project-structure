from extensions import db


class KlineException(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exchange = db.Column(db.VARCHAR, )
    coin_pair = db.Column(db.VARCHAR, )
    status = db.Column(db.VARCHAR, )

    def get_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
