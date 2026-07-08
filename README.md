# Nippon Detail & Custom — Management System

A management system built for an automotive detailing business, covering client and vehicle management, service tracking, inventory control, and a public-facing site with an instant-quote form.

---

## About

Nippon Detail & Custom is a system built to manage the day-to-day operations of an automotive detailing shop. It allows registering clients and their vehicles, tracking services performed, managing materials and purchases, and viewing delivery deadlines on a calendar — plus a public site where prospective clients can request a quote pre-filled straight into WhatsApp.

**Development notes:** the backend (models, schemas, routes, auth, database) was built entirely by me. The frontend (HTML/CSS/JS) was built with AI assistance (Claude), based on my own layout references, business requirements, and design decisions.

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
│   │   ├── client.py
│   │   ├── vehicle.py
│   │   ├── service.py
│   │   └── material.py
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── css/
│   │   ├── global.css
│   │   └── central.css
│   ├── js/
│   │   ├── script.js
│   │   └── central.js
│   ├── img/
│   └── templates/
│       ├── index.html
│       └── central.html
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

# Create a .env file with:
#   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/nippon_db
#   SECRET_KEY=your_secret_key
#   ALGORITHM=HS256

# Run the server
python -m uvicorn main:app --reload
```

Access the API at: **http://localhost:8000**
Interactive docs at: **http://localhost:8000/docs**
Frontend: open `frontend/templates/index.html` with Live Server on port **5500**

The database schema is created automatically on first run via SQLAlchemy's `Base.metadata.create_all()` — no manual migration needed.

---

## API Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/register` | Register a new admin user. **Requires an existing valid token** — there's no public sign-up; the first account is seeded directly in the database. |
| POST | `/auth/login` | Authenticate and receive JWT token (OAuth2 form-data) |

### Clients
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/client/register` | Register a new client |
| GET | `/client/get/all` | List all clients |
| GET | `/client/get/id/{id}` | Get client by ID |
| GET | `/client/get/expired/{bool}` | List active or expired clients |
| GET | `/client/get/incomplete` | List clients with missing contact/address info |
| PUT | `/client/update/{id}` | Full update of a client |
| PATCH | `/client/update/expired/{id}` | Toggle client expired status (cascades: deactivates the client's vehicles and marks their services as finished) |
| DELETE | `/client/delete/{id}` | Delete a client |

### Vehicles
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/vehicle/register` | Register a new vehicle linked to a client |
| GET | `/vehicle/get/all` | List all vehicles |
| GET | `/vehicle/get/id/{id}` | Get vehicle by ID |
| GET | `/vehicle/get/active/{bool}` | List active or inactive vehicles |
| PUT | `/vehicle/update/{id}` | Full update of a vehicle |
| PATCH | `/vehicle/update/active/{id}` | Toggle vehicle active status |
| DELETE | `/vehicle/delete/{id}` | Delete a vehicle |

### Services
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/service/register` | Register a new service linked to a client and vehicle |
| GET | `/services/get/all` | List all services |
| GET | `/service/get/{id}` | Get service by ID |
| GET | `/services/get/{finish}` | List finished or pending services |
| PUT | `/service/update/{id}` | Full update of a service |
| PATCH | `/service/update/finish/{id}` | Toggle service finish status |
| DELETE | `/service/delete/{id}` | Delete a service |

### Materials
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/material/register` | Register a new material |
| GET | `/material/get/all` | List all materials |
| GET | `/material/get/id/{id}` | Get material by ID |
| GET | `/material/get/expired/{bool}` | List expired or valid materials |
| GET | `/material/get/available/{bool}` | List available or unavailable materials |
| PUT | `/material/update/{id}` | Full update of a material |
| PATCH | `/material/update/stock/{id}` | Update material stock (quantity and value) |
| PATCH | `/material/update/available/{id}` | Toggle material available status |
| PATCH | `/material/update/expired/{id}` | Toggle material expired status |
| DELETE | `/material/delete/{id}` | Delete a material |

### Error Handling

All routes return a `404` with a specific `detail` message when a referenced record (client, vehicle, service, material) doesn't exist. Creating or updating a `Client` (unique `cpf`/`email`) or a `Vehicle` (unique `plate`) returns a `409 Conflict` with a specific `detail` message if the value is already registered to another record, instead of a raw database error.

---

## Data Models

### User
| Field | Type | Description |
|-------|------|-------------|
| user_id | Integer | Primary key |
| username | String | Unique username |
| pass_hash | String | Hashed password (bcrypt) |

There is no public registration flow — the first (and, for now, only) account is inserted directly into the database, with the password hashed via `passlib`'s bcrypt context beforehand. All authenticated requests share the same database; there's no per-user data isolation.

### Client
| Field | Type | Description |
|-------|------|-------------|
| client_id | Integer | Primary key |
| name | String | Client full name |
| cpf | String | Unique Brazilian tax ID |
| cep | String (optional) | Postal code |
| address | String (optional) | Full address |
| email | String (optional) | Client email |
| tel | String (optional) | Phone number |
| expired | Boolean | Whether the client is inactive |
| created | DateTime | Registration timestamp |

### Vehicle
| Field | Type | Description |
|-------|------|-------------|
| vehicle_id | Integer | Primary key |
| client_id | Integer | Foreign key → clients |
| model | String | Vehicle model |
| plate | String | Unique license plate |
| kind | String (optional) | Vehicle type (car, motorcycle, etc.) |
| active | Boolean | Whether the vehicle is active |
| created | DateTime | Registration timestamp |

### Service
| Field | Type | Description |
|-------|------|-------------|
| service_id | Integer | Primary key |
| vehicle_id | Integer | Foreign key → vehicles |
| client_id | Integer | Foreign key → clients |
| title | String | Service title |
| desc | String | Service description |
| kind | String | Service type |
| date_release | DateTime (optional) | Expected delivery date |
| value | Float | Service price |
| finish | Boolean | Whether the service is completed |
| created | DateTime | Registration timestamp |

### Material
| Field | Type | Description |
|-------|------|-------------|
| material_id | Integer | Primary key |
| name | String | Material name |
| mark | String | Brand/manufacturer |
| quantity | Integer | Current stock quantity |
| value | Float | Unit price |
| total_value | Float (computed) | Calculated automatically as quantity × value |
| date_available | DateTime (optional) | Expiration date |
| expired | Boolean | Whether the material is expired |
| available | Boolean | Whether the material is available for use |

---

## Data Integrity

- **Deleting** a client or vehicle cascades automatically via SQLAlchemy `relationship(cascade="all, delete-orphan")` — deleting a client removes its vehicles, which in turn removes their services.
- **Deactivating** a client (`expired=true`) manually deactivates their vehicles and marks their pending services as finished (to preserve historical/financial records instead of deleting them).

---

## Frontend Overview

- **Public site** (`templates/index.html`): landing page with an image carousel (subtle Ken Burns zoom on the active slide), service showcase, and a scroll-spy navbar (active link updates automatically as you scroll, including a fix for the last section on the page). Includes a mobile hamburger menu below 900px, scroll-triggered reveal animations on each section, and a light/dark theme toggle (persisted for the duration of the browser tab via `sessionStorage`, always starts in dark mode on a fresh visit). A "Peça seu orçamento" button (in the navbar and in the hero) opens a form — name, CPF, phone, e-mail, address, vehicle, and desired service — that builds a pre-filled WhatsApp message and opens it in a new tab; nothing is saved to the database. There's no public sign-up anymore, only a login button for the shop's admin account.
- **Admin area** (`templates/central.html`): single-page app with a sidebar (Dashboard, Calendar, Clients, Vehicles, Services, Materials, Status) — views are swapped via JavaScript without page reloads. Includes CRUD for all entities, an edit/delete selection mode, detail modals, dashboard stats, a monthly/yearly delivery calendar (color-coded per client, hover preview, click-through to the service), an initial loading overlay, and disabled/spinner state on save buttons to prevent duplicate submissions. Clicking the sidebar logo returns to the public site. Shares the same theme toggle as the public site.

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

🚧 In development — core backend and frontend MVP functional, including public site content (About/Contact), light/dark theme, a delivery calendar view, a WhatsApp-based quote form, and a PostgreSQL database; pending: financial overview (revenue vs. expenses, with an auto-generated expense entry on material restock) and deployment to production hosting.