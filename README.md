# Travel Planner | DevelopsToday Test Task

Small FastAPI application developed as a test task. The project uses SQLite for storage, integrates with the Art Institute of Chicago API, and can be run either locally or through Docker.

## Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
DATABASE_URL=sqlite+aiosqlite:///./travel.db
AIC_BASE_URL=https://api.artic.edu/api/v1
AUTH_USERNAME=admin
AUTH_PASSWORD=secret
```

## Running with Docker

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

To stop the containers:

```bash
docker compose down
```

## Running locally

Create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure the `.env` file is present, then start the server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

## API documentation

FastAPI provides interactive API documentation out of the box:

* Swagger UI: `http://localhost:8000/docs`

## Notes

* The project uses SQLite, so the database is stored in the `travel.db` file.
* When running with Docker, the database file is mounted as a volume to preserve data between container restarts.
* Default credentials can be changed through the `.env` file.
