import json
import pytest
from main.models import Client, Parking, ClientParking


def test_math_route(client) -> None:
    resp = client.get("/test_route/8")
    data = json.loads(resp.data.decode())
    assert data == 64


@pytest.fixture
def test_data(db):
    """Создает тестовые данные для тестов парковки"""
    client_ = Client(
        name="Тест",
        surname="Тестов",
        credit_card="1234567890123456",
        car_number="А123БВ"
    )

    parking = Parking(
        address="Тестовая улица, 1",
        opened=True,
        count_places=10,
        count_available_places=5
    )

    db.session.add(client_)
    db.session.add(parking)
    db.session.commit()

    return {"client_id": client_.id, "parking_id": parking.id}


@pytest.mark.parametrize("route", [
    "/test_route/5",
    "/clients",
    "/clients/1",
])
def test_get_routes_return_200(client, route):
    """Проверка, что все GET-маршруты возвращают код 200"""
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client, db):
    """Тест создания клиента"""
    client_data = {
        "name": "Петр",
        "surname": "Петров",
        "credit_card": "9876543210987654",
        "car_number": "В456ГД"
    }

    response = client.post("/clients", data=client_data)

    assert response.status_code == 201

    created_client = Client.query.filter_by(
        name="Петр",
        surname="Петров"
    ).first()

    assert created_client is not None
    assert created_client.credit_card == "9876543210987654"
    assert created_client.car_number == "В456ГД"


def test_create_parking(client, db):
    """Тест создания парковки"""
    parking_data = {
        "address": "Новая улица, 10",
        "opened": True,
        "count_places": 20,
        "count_available_places": 15
    }

    response = client.post("/parking", data=parking_data)

    assert response.status_code == 201

    created_parking = Parking.query.filter_by(
        address="Новая улица, 10"
    ).first()

    assert created_parking is not None
    assert created_parking.opened == True
    assert created_parking.count_places == 20
    assert created_parking.count_available_places == 15


@pytest.mark.parking
def test_parking_entry(client, db, test_data):
    """Тест заезда на парковку"""
    client_id = test_data["client_id"]
    parking_id = test_data["parking_id"]

    parking = db.session.get(Parking, parking_id)
    available_before = parking.count_available_places

    response = client.post("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Заезд на парковку совершен"

    parking_after = db.session.get(Parking, parking_id)
    assert parking_after.count_available_places == available_before - 1

    entry = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first()

    assert entry is not None
    assert entry.time_in is not None


@pytest.mark.parking
def test_parking_exit(client, db, test_data):
    """Тест выезда с парковки"""
    client_id = test_data["client_id"]
    parking_id = test_data["parking_id"]

    client.post("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })

    parking = db.session.get(Parking, parking_id)
    available_before = parking.count_available_places

    response = client.delete("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Выезд зарегистрирован"

    parking_after = db.session.get(Parking, parking_id)
    assert parking_after.count_available_places == available_before + 1

    entry = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id
    ).first()

    assert entry.time_out is not None
    assert entry.time_out > entry.time_in


@pytest.mark.parking
def test_parking_entry_no_spaces(client, db, test_data):
    """Тест заезда при отсутствии свободных мест"""
    client_id = test_data["client_id"]
    parking_id = test_data["parking_id"]

    parking = db.session.get(Parking, parking_id)
    parking.count_available_places = 0
    db.session.commit()

    response = client.post("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Нет свободных мест на парковке"

    parking.count_available_places = 5
    db.session.commit()


@pytest.mark.parking
def test_parking_entry_closed(client, db, test_data):
    """Тест заезда на закрытую парковку"""
    client_id = test_data["client_id"]
    parking_id = test_data["parking_id"]

    parking = db.session.get(Parking, parking_id)
    parking.opened = False
    db.session.commit()

    response = client.post("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Парковка закрыта"

    parking.opened = True
    db.session.commit()
