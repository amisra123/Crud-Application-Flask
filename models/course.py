from db import db
import datetime

class CourseModel(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    description = db.Column(db.String(255))
    discount_price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(100))
    on_discount = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)

    def __init__(self, description, discount_price, image_path, on_discount, price, title):
        self.description = description
        self.discount_price = discount_price
        self.image_path = image_path
        self.on_discount = on_discount
        self.date_updated = datetime.datetime.utcnow()
        self.price = price
        self.title = title

    def json(self):
        return {'id': self.id,'date_created': str(self.date_created), 'date_updated': str(self.date_updated), 'description': self.description, 'discount_price' : self.discount_price, 'image_path': self.image_path, 'on_discount': self.on_discount,
                'price': self.price, 'title': self.title}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def find_by_title(title):
        return CourseModel.query.filter(CourseModel.title.like("%" + title + "%")).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def add_data_to_db(self):
        db.session.add(self)
        db.session.commit()




