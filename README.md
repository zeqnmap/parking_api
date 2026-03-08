# Parking Management API

A RESTful API for parking management built with Flask and SQLAlchemy. The system allows managing clients, parking spaces, and tracking vehicle entry/exit.

## 🚀 Features

- **Client Management**: Create and retrieve client information (name, surname, credit card, car number)
- **Parking Management**: Create and manage parking lots with available spot tracking
- **Entry/Exit Tracking**: Record vehicle entry and exit times
- **Availability Control**: Automatic updates of available parking spots
- **Credit Card Validation**: Support for clients with/without payment cards

## 🛠 Tech Stack

- **Backend**: Flask (Python 3.8+)
- **Database**: SQLite with SQLAlchemy ORM
- **Testing**: Pytest with Factory Boy
- **API Style**: RESTful

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/test_route/<int:num>` | Test endpoint (returns square of number) |
| GET | `/clients` | Get all clients |
| GET | `/clients/<int:client_id>` | Get client by ID |
| POST | `/clients` | Create new client (form-data) |
| POST | `/parking` | Create new parking (form-data) |
| POST | `/client_parking` | Record vehicle entry (JSON) |
| DELETE | `/client_parking` | Record vehicle exit (JSON) |

## 🏁 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd module_29_testing/hw
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install requirements.txt
```

4. Run the application
```bash
python main/app.py
```

The server will start at `http://localhost:5000`

## 🧪 Testing

The project includes comprehensive tests using pytest and Factory Boy.

### Test Structure
- **Unit Tests**: Test individual components
- **Integration Tests**: Test API endpoints
- **Factory Tests**: Test data factories

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_flask.py -v

# Run tests with parking marker
pytest tests/ -m parking -v

# Run with coverage report
pytest tests/ --cov=main -v
```

### Test Coverage
- ✅ GET routes status code 200
- ✅ Client creation
- ✅ Parking creation
- ✅ Vehicle entry (with parking spot availability check)
- ✅ Vehicle exit (with parking spot release)
- ✅ Error handling (closed parking, no spots, missing entries)

## 🏗 Project Structure

```
parking_api/
├── main/
│   ├── __init__.py
│   ├── app.py           # Flask application
│   └── models.py         # SQLAlchemy models
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   ├── factories.py      # Factory Boy factories
│   ├── test_flask.py     # API endpoint tests
│   └── test_factories.py # Factory tests
├── pytest.ini            # Pytest configuration
|__ requirements.txt      # Needed libraries
└── README.md             # You here
```

## 📊 Database Models

### Client
- `id`: Integer (Primary Key)
- `name`: String(50) (Required)
- `surname`: String(50) (Required)
- `credit_card`: String(50) (Optional)
- `car_number`: String(10)

### Parking
- `id`: Integer (Primary Key)
- `address`: String(100) (Required)
- `opened`: Boolean
- `count_places`: Integer (Total spots)
- `count_available_places`: Integer (Available spots)

### ClientParking (Junction Table)
- `id`: Integer (Primary Key)
- `client_id`: Foreign Key to Client
- `parking_id`: Foreign Key to Parking
- `time_in`: DateTime
- `time_out`: DateTime (NULL if still parked)

## 🔒 Business Rules

- Client cannot park if parking is closed
- Client cannot park if no spots available
- Available spots decrease on entry, increase on exit
- Client cannot have multiple active parking sessions
- Exit time must be after entry time

## 🎯 Usage Examples

### Create a client
```bash
curl -X POST http://localhost:5000/clients \
  -F "name=John" \
  -F "surname=Doe" \
  -F "credit_card=1234567890123456" \
  -F "car_number=А123БВ"
```

### Create a parking
```bash
curl -X POST http://localhost:5000/parking \
  -F "address=123 Main St" \
  -F "opened=true" \
  -F "count_places=50" \
  -F "count_available_places=50"
```

### Record vehicle entry
```bash
curl -X POST http://localhost:5000/client_parking \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "parking_id": 1}'
```

### Record vehicle exit
```bash
curl -X DELETE http://localhost:5000/client_parking \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "parking_id": 1}'
```

---

## **🏁 Author: zeqnmap**