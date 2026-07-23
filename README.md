# Mulika Invoice Generator

GST invoice management platform for Indian SMBs. Monorepo with two backend services and a frontend.

```
mulika_invoice/
├── auth-service/            # Java Spring Boot — users, JWT issuance, roles (Pratik)
├── invoice-engine-service/  # Python FastAPI — customers, products, invoices, GST, PDF (Xarvis)
├── frontend/                # React app (in progress)
└── JWT_CONTRACT.md          # Shared JWT claim contract between both services
```

## Running invoice-engine-service locally

```bash
cd invoice-engine-service
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# create .env with DATABASE_URL=...
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## Running auth-service locally

```bash
cd auth-service
./mvnw spring-boot:run
```

Both services connect to the same PostgreSQL database (`mulika_dev`) and must share the same JWT signing secret — see `JWT_CONTRACT.md`. The secret is passed via environment variable in each service, never committed to Git.
