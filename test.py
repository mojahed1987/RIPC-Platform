from dotenv import load_dotenv
import os

from core.requests.client import RIPCClient
from core.logging.logger import setup_logger

load_dotenv()

logger = setup_logger("RIPC")

TOKEN = os.getenv("RIPC_TOKEN")

logger.info(f"TOKEN EXISTS : {TOKEN is not None}")
logger.info(f"TOKEN START  : {TOKEN[:10] if TOKEN else 'NO TOKEN'}")

logger.info("Starting RIPC Test")

client = RIPCClient(TOKEN)

payload = {}

response = client.post(
    "/ps-be/v3/api/project/browse?page=1&size=1&sort=",
    payload
)

logger.info(f"STATUS CODE : {response.status_code}")

print(response.text[:1000])