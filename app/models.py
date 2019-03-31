from app import db


class Entries(db.Model):
    """ Модель для views.just_another_parser_v1 """

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    all_tags = db.Column(db.Integer, nullable=False)
    a_tags = db.Column(db.Integer, nullable=False)
    div_tags = db.Column(db.Integer, nullable=False)

