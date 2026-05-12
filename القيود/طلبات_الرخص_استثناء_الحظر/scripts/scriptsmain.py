import os
import re
import json
import pandas as pd
from datetime import datetime

from core.auth.otp_auth import get_token
from core.requests.client import RIPCClient
from core.utils.save import save_json, save_excel


# ==================================================
# PATHS
# ==================================================
BASE_DIR = r"C:\RIPC_NEW\القيود\طلبات_الرخص_استثناء_الحظر"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TODAY = datetime.now().strftime("%Y%m%d_%H%M%S")

JSON_PATH = os.path.join(OUTPUT_DIR, f"restriction_requests_{TODAY}.json")
EXCEL_PATH = os.path.join(OUTPUT_DIR, f"restriction_requests_{TODAY}.xlsx")


# ==================================================
# REQUEST IDS
# ضع هنا أرقام الطلبات فقط
# ==================================================
raw_ids = """
63053
63430
63752
63755
63874
63968
63985
63993
64012
64011
63949
63909
63911
63910
63923
63921
"""


# ==================================================
# HELPERS
# ==================================================
def clean_request_ids(raw_text):
    ids = re.findall(r"\d+", raw_text)
    return list(dict.fromkeys(ids))


def flatten_json(data, parent_key="", sep="_"):
    rows = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key

            if isinstance(value, dict):
                rows.update(flatten_json(value, new_key, sep=sep))

            elif isinstance(value, list):
                rows[new_key] = json.dumps(value, ensure_ascii=False)

            else:
                rows[new_key] = value

    return rows


def extract_data(response_json):
    if isinstance(response_json, dict):
        if "data" in response_json:
            return response_json.get("data")
        return response_json

    return response_json


# ==================================================
# API FUNCTIONS
# عدل endpoint حسب رابط API الصحيح عندك
# ==================================================
def get_request_details(client, request_id):
    endpoint = f"/gateway/ps-be/v3/api/restriction-request/{request_id}"

    response = client.get(endpoint)

    if client.is_token_expired(response):
        return {
            "request_id": request_id,
            "status": "TOKEN_EXPIRED",
            "http_status": response.status_code,
            "error": response.text
        }

    if response.status_code != 200:
        return {
            "request_id": request_id,
            "status": "FAILED",
            "http_status": response.status_code,
            "error": response.text
        }

    try:
        response_json = response.json()
        data = extract_data(response_json)

        flat = flatten_json(data)
        flat["request_id_input"] = request_id
        flat["http_status"] = response.status_code
        flat["status"] = "OK"

        return flat

    except Exception as e:
        return {
            "request_id": request_id,
            "status": "JSON_ERROR",
            "http_status": response.status_code,
            "error": str(e),
            "raw_text": response.text
        }


# ==================================================
# MAIN
# ==================================================
def main():
    print("=" * 60)
    print("RIPC Restriction Requests")
    print("=" * 60)

    token = get_token()

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "").strip()

    client = RIPCClient(token)

    request_ids = clean_request_ids(raw_ids)

    print(f"TOTAL REQUEST IDS: {len(request_ids)}")
    print("=" * 60)

    results = []

    for index, request_id in enumerate(request_ids, start=1):
        print(f"[{index}/{len(request_ids)}] Fetching {request_id} ...")

        row = get_request_details(client, request_id)
        results.append(row)

        if row.get("status") == "TOKEN_EXPIRED":
            print("=" * 60)
            print("TOKEN EXPIRED - saved previous results")
            print("=" * 60)
            break

    save_json(results, JSON_PATH)
    save_excel(results, EXCEL_PATH)

    print("=" * 60)
    print("DONE")
    print(JSON_PATH)
    print(EXCEL_PATH)
    print("=" * 60)


if __name__ == "__main__":
    main()