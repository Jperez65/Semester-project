from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

                      
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    middle_initial= db.Column(db.String)
    afiliation = db.Column(db.String)
    department= db.Column(db.String)
    country = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    email_address = db.Column(db.String)
    phone_number = db.Column(db.String)


@classmethod
def create_user(dict_user_data):
    pass
    # db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})