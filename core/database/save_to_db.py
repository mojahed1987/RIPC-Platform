import json
from sqlalchemy import text

from core.database.connection import engine


def save_restriction_exception(row):
    sql = text("""
        INSERT INTO restriction_exceptions
        (request_id, status, http_status, raw_data)
        VALUES
        (:request_id, :status, :http_status, :raw_data)
    """)

    with engine.begin() as conn:
        conn.execute(sql, {
            "request_id": str(row.get("request_id") or row.get("request_id_input")),
            "status": row.get("status"),
            "http_status": row.get("http_status"),
            "raw_data": json.dumps(row, ensure_ascii=False)
        })


def save_restriction_exceptions(rows):
    for row in rows:
        save_restriction_exception(row)

    print(f"SAVED TO DATABASE: {len(rows)} rows")