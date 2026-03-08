from .app import db
from typing import Dict, Any


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))
    parking = db.relationship('ClientParking', backref='client', lazy=True)

    def __repr__(self):
        return f"Клиент: {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    clients = db.relationship('ClientParking', backref='parking', lazy=True)

    def __repr__(self):
        return f"Парковка: {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=True)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    def __repr__(self):
        return f"Запись парковки: клиент {self.client_id} на парковке {self.parking_id}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}