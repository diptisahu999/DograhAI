import json
import os

# Set dummy env vars to avoid startup errors
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///dummy.db"
os.environ["MINIO_ENDPOINT"] = "localhost"
os.environ["MINIO_ACCESS_KEY"] = "admin"
os.environ["MINIO_SECRET_KEY"] = "admin"
os.environ["REDIS_URL"] = "redis://localhost"

from api.app import app

with open("ui/openapi.json", "w") as f:
    json.dump(app.openapi(), f)
