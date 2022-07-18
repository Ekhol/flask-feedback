from app import app
from models import db

db.drop_all()
db.create_all()
db.session.add_all()
db.session.commit()
