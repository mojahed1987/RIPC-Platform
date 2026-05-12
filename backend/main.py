from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from core.database.connection import engine

app = FastAPI(title="RIPC Platform API")


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

    html = f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <title>RIPC Platform</title>

        <style>

            body {{

                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f6fa;

            }}

            h1 {{

                color: #2c3e50;

            }}

            table {{

                border-collapse: collapse;
                width: 100%;
                background: white;

            }}

            th, td {{

                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;

            }}

            th {{

                background-color: #2c3e50;
                color: white;

            }}

            tr:nth-child(even) {{

                background-color: #f2f2f2;

            }}

            tr:hover {{

                background-color: #e8f0fe;

            }}

        </style>

    </head>

    <body>

        <h1>RIPC Restriction Exceptions Dashboard</h1>

        <table>

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

    return html