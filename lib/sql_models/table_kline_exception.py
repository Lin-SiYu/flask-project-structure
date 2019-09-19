from extensions import db
from lib.sql_models.base_model import BaseModel


class KlineException(BaseModel):
    exchange = db.Column(db.VARCHAR, )
    coin_pair = db.Column(db.VARCHAR, )
    period = db.Column(db.VARCHAR, )
    from_time = db.Column(db.VARCHAR, )
    end_time = db.Column(db.VARCHAR, )
    status = db.Column(db.VARCHAR, )
