# Nippon Detail & Custom — Management System

A full-stack management system built for an automotive detailing business, covering vehicle and service management, inventory control, and financial tracking.

---

## About

Nippon Detail & Custom is a system built to manage the day-to-day operations of an automotive detailing shop. It allows registering clients and their vehicles, tracking services performed, managing materials and purchases, and monitoring the shop's financial overview through automatic cost calculations.

---

## Project Structure

```
nippon-system/
├── backend/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── vehicle.py
│   │   ├── service.py
│   │   └── material.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── vehicle.py
│   │   ├── service.py
│   │   └── material.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── vehicle.py
│   │   ├── service.py
│   │   └── material.py
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── css/
│   │   └── global.css
│   ├── js/
│   │   └── script.js
│   ├── index.html
│   └── central.html
├── .gitignore
└── README.md
```

---

## Installation

**Requirements:** Python 3.8+, PostgreSQL

```bash
# Clone the repository
git clone https://github.com/felipebsa/nippon-system.git
cd nippon-system/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload
```

Access the API at: **http://localhost:8000**  
Interactive docs at: **http://localhost:8000/docs**  
Frontend: open `frontend/index.html` with Live Server on port **5500**

---

## API Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/login` | Authenticate and receive JWT token |
| POST | `/auth/register` | Register and create JWT token |
|--------|-------|-------------|
| | | |

### Clients
| Method | Route | Description |
|--------|-------|-------------|
| | | |

### Vehicles
| Method | Route | Description |
|--------|-------|-------------|
| | | |

### Services
| Method | Route | Description |
|--------|-------|-------------|
| | | |

### Materials
| Method | Route | Description |
|--------|-------|-------------|
| | | |

---

## Data Models

### User
| Field | Type | Description |
|-------|------|-------------|
| | | |

### Client
| Field | Type | Description |
|-------|------|-------------|
| | | |

### Vehicle
| Field | Type | Description |
|-------|------|-------------|
| | | |

### Service
| Field | Type | Description |
|-------|------|-------------|
| | | |

### Material
| Field | Type | Description |
|-------|------|-------------|
| | | |

---

## Tech Stack

**Backend**
- [Python 3](https://python.org)
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0](https://sqlalchemy.org)
- [Pydantic](https://docs.pydantic.dev)
- [PostgreSQL](https://postgresql.org)
- [Uvicorn](https://www.uvicorn.org)

**Frontend**
- HTML5 / CSS3
- Vanilla JavaScript (Fetch API)

---

## Status

🚧 In development
