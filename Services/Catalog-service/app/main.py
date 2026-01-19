from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="Catalog Service")

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            price INT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            ("Laptop", 1200)
        )

    conn.commit()

    cur.execute("SELECT id, name, price FROM products")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]
