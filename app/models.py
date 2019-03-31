from app import db


class Entries(db.Model):
    """ Модель для views.just_another_parser_v1 """

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250))
    all_tags = db.Column(db.Integer)
    a_tags = db.Column(db.Integer)
    div_tags = db.Column(db.Integer)


class DentistContacts(db.Model):

    """ Model for storing dentist clinics information in Webscraping Selenium project """

    __tablename__ = 'dentist_contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250))
    website = db.Column(db.String(100))
    phone = db.Column(db.String(50))
