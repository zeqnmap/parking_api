import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
from main.app import create_app, db as _db
from main.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()

        client_ = Client(
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="car_num")

        parking = Parking(
            address="address",
            opened=True,
            count_places=5,
            count_available_places=3)

        _db.session.add(client_)
        _db.session.add(parking)
        _db.session.commit()

        client_parking = ClientParking(
           client_id=client_.id,
           parking_id=parking.id,
           time_in=datetime.now(),
           time_out=datetime.now())

        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def test_data(db):
    """Возвращает id тестовых клиента и парковки"""
    client_ = Client.query.filter_by(name="name").first()
    parking = Parking.query.filter_by(address="address").first()
    return {"client_id": client_.id, "parking_id": parking.id}
