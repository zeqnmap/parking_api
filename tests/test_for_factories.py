from main.models import Client, Parking
from tests.factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(db):
    """Тест создания клиента с использованием ClientFactory"""
    client = ClientFactory()

    # клиент создан и сохранен в БД
    assert client.id is not None
    assert client.name is not None
    assert client.surname is not None

    client_from_db = db.session.get(Client, client.id)
    assert client_from_db == client


def test_create_client_with_credit_card(db):
    """Тест создания клиента с кредитной картой"""
    client = ClientFactory(credit_card="1234567890123456")
    assert client.credit_card == "1234567890123456"

    client_from_db = db.session.get(Client, client.id)
    assert client_from_db.credit_card == "1234567890123456"


def test_create_client_without_credit_card(db):
    """Тест создания клиента без кредитной карты"""
    client = ClientFactory(credit_card=None)
    assert client.credit_card is None

    client_from_db = db.session.get(Client, client.id)
    assert client_from_db.credit_card is None


def test_create_multiple_clients(db):
    """Тест создания нескольких клиентов через фабрику"""
    clients = ClientFactory.create_batch(5)

    assert len(clients) == 5
    for client in clients:
        assert client.id is not None

    assert Client.query.count() >= 5


def test_create_parking_with_factory(db):
    """Тест создания парковки с использованием ParkingFactory"""
    parking = ParkingFactory()

    assert parking.id is not None
    assert parking.address is not None
    assert parking.count_places > 0
    assert parking.count_available_places <= parking.count_places

    parking_from_db = db.session.get(Parking, parking.id)
    assert parking_from_db == parking


def test_create_parking_with_specific_values(db):
    """Тест создания парковки с конкретными значениями"""
    parking = ParkingFactory(
        address="ул. Тестовая, 1",
        opened=True,
        count_places=50,
        count_available_places=25
    )

    assert parking.address == "ул. Тестовая, 1"
    assert parking.opened is True
    assert parking.count_places == 50
    assert parking.count_available_places == 25


def test_parking_lazy_attribute(db):
    """Тест LazyAttribute для count_available_places"""
    for _ in range(10):
        parking = ParkingFactory()
        assert parking.count_available_places <= parking.count_places
        assert parking.count_available_places >= 0


def test_create_multiple_parking(db):
    """Тест создания нескольких парковок через фабрику"""
    parkings = ParkingFactory.create_batch(5)

    assert len(parkings) == 5
    for parking in parkings:
        assert parking.id is not None

    assert Parking.query.count() >= 5
