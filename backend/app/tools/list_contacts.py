import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

CONTACTS_PATH = Path(__file__).resolve().parents[3] / "data" / "contacts.json"

def list_contacts() -> dict:
    with CONTACTS_PATH.open("r", encoding="utf-8") as f:

        data = json.load(f)
        print(f"[DATA]: {str(data)}")

        contacts = data.get("contacts", [])
        print(f"[CONTACTS]: {str(contacts)}")

        if not contacts : 
            logger.warning(f"[ERROR]: cannot find the contact info")
            return json.dumps({"error": "cannot find the contact info"})

        return json.dumps(data)
    