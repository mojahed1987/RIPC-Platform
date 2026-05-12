import sys

BASE_DIR = r"C:\RIPC_NEW\القيود\طلبات_الرخص_استثناء_الحظر"
sys.path.append(BASE_DIR)

from api.get_details import get_request_details

print("=" * 50)
print("RIPC Restriction System")
print("=" * 50)

request_id = 86141

data = get_request_details(request_id)

print(data)