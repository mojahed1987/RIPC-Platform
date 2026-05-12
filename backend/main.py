from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from core.database.connection import engine


app = FastAPI(title="RIPC Platform API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "RIPC Platform API is running"
    }


@app.get("/restrictions")
def get_restrictions():
    sql = text("""
        SELECT
            id,
            request_id,
            status,
            http_status,
            created_at
        FROM restriction_exceptions
        ORDER BY id DESC
        LIMIT 100
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()

    return list(rows)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    sql = text("""
        SELECT
            id,
            request_id,
            status,
            http_status,
            created_at
        FROM restriction_exceptions
        ORDER BY id DESC
        LIMIT 100
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()

    html_rows = ""

    for row in rows:
        html_rows += f"""
        <tr>
            <td>{row["id"]}</td>
            <td>{row["request_id"]}</td>
            <td>{row["status"]}</td>
            <td>{row["http_status"]}</td>
            <td>{row["created_at"]}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RIPC Platform</title>
    </head>
    <body>
        <h1>RIPC Restriction Exceptions Dashboard</h1>
        <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
            <tr>
                <th>ID</th>
                <th>Request ID</th>
                <th>Status</th>
                <th>HTTP Status</th>
                <th>Created At</th>
            </tr>
            {html_rows}
        </table>
    </body>
    </html>
    """