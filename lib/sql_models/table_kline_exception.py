from extensions import db


class KlineException(db.BaseModel):
    exchange = db.Column(db.VARCHAR, )
    coin_pair = db.Column(db.VARCHAR, )
    status = db.Column(db.VARCHAR, )
