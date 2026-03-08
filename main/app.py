from datetime import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///prod.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/test_route/<int:num>", methods=['GET'])
    def math_route(num: int):
        """Тестовый роут для расчета степени"""
        result = num ** 2
        return jsonify(result)


    @app.route("/clients", methods=['GET'])
    def get_list_clients():
        """Получить список всех клиентов"""
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [c.to_json() for c in clients]
        return jsonify(clients_list), 200


    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_client_handler(client_id: int):
        """Получение клиента по id"""
        client: Client = db.session.get(Client, client_id)
        return jsonify(client.to_json()), 200


    @app.route("/clients", methods=['POST'])
    def create_client_handler():
        """Создание нового клиента"""
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        car_number = request.form.get('car_number', type=str)

        new_client = Client(name=name,
                            surname=surname,
                            credit_card=credit_card,
                            car_number=car_number)

        db.session.add(new_client)
        db.session.commit()

        return '', 201


    @app.route("/parking", methods=['POST'])
    def create_parking_handler():
        """Создание нового парковочного места"""
        address = request.form.get('address', type=str)
        opened = request.form.get('opened', type=bool)
        count_places = request.form.get('count_places', type=int)
        count_available_places = request.form.get('count_available_places', type=int)

        new_parking = Parking(address=address,
                            opened=opened,
                            count_places=count_places,
                            count_available_places=count_available_places)

        db.session.add(new_parking)
        db.session.commit()

        return '', 201


    @app.route("/client_parking", methods=['POST'])
    def create_client_entry():
        """Заезд клиента на парковку"""
        data = request.get_json()
        if not data:
            return jsonify(error="Требуется JSON"), 400

        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        client = db.session.get(Client, client_id)
        if not client:
            return jsonify(error="Клиент не найден"), 404

        parking = db.session.get(Parking, parking_id)
        if not parking:
            return jsonify(error="Парковка не найдена"), 404

        if not parking.opened:
            return jsonify(error="Парковка закрыта"), 400

        if parking.count_available_places <= 0:
            return jsonify(error="Нет свободных мест на парковке"), 400

        parking.count_available_places -= 1

        parking_entry = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.now(),
            time_out=None
        )

        db.session.add(parking_entry)
        db.session.commit()

        return jsonify({'message': 'Заезд на парковку совершен'})


    @app.route("/client_parking", methods=['DELETE'])
    def delete_client_entry():
        """Выезд клиента с парковки"""
        data = request.get_json()
        if not data:
            return jsonify(error="Требуется JSON"), 400

        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        if not client_id or not parking_id:
            return jsonify(error="Не указаны client_id или parking_id"), 400

        parking = db.session.get(Parking, parking_id)
        if not parking:
            return jsonify(error="Парковка не найдена"), 404

        active_entry = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first()

        if not active_entry:
            return jsonify(error="Заезд на паркинг не найден"), 404

        parking.count_available_places += 1

        active_entry.time_out = datetime.now()

        db.session.commit()

        return jsonify({"message": "Выезд зарегистрирован"}), 200

    return app