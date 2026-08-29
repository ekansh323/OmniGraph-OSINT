# Database setup

Milestone 2 uses Alembic migrations as the only schema source of truth. Run these commands from the repository root.

```powershell
docker compose up -d postgres
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini upgrade head
.\.venv\Scripts\python.exe database\seed.py
```

To verify the schema and seed data:

```powershell
.\.venv\Scripts\python.exe -m pytest database\tests
```

The seed command is intentionally limited to two small synthetic cases and six entities. Loading the complete Milestone 1 evidence set is deferred until the evidence-processing milestone.
