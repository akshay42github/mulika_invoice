from fastapi import FastAPI
from app.routers import customers, products, invoices, invoice_line_items


app = FastAPI(title="Mulika Invoice Engine")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(invoices.router)
app.include_router(invoice_line_items.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

    