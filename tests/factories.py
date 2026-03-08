import factory
from main.models import Client, Parking
import random
from main.app import db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')

    credit_card = factory.LazyAttribute(
        lambda _: random.choice([
            None,
            f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
            f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        ])
    )

    car_number = factory.LazyAttribute(
        lambda _: f"{random.choice('АВЕКМНОРСТУХ')}{random.randint(100, 999)}"
               f"{random.choice('АВЕКМНОРСТУХ')}{random.choice('АВЕКМНОРСТУХ')}"
    )


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.Faker('street_address')
    opened = factory.LazyAttribute(lambda _: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda _: random.randint(10, 200))

    count_available_places = factory.LazyAttribute(
        lambda o: random.randint(0, o.count_places)
    )