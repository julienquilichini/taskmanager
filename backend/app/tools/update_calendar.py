"""Google Calendar tool: create / update events via a service account.

One-time setup: share the target calendar with the service account email
(see `client_email` in the credentials JSON) with the "Make changes to
events" permission, then set GOOGLE_CALENDAR_ID in .env.
"""

import json
from datetime import datetime
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core import config


####################################################################################################
### CONSTANTS
####################################################################################################

SCOPES = ["https://www.googleapis.com/auth/calendar"]


####################################################################################################
### INTERNAL HELPERS
####################################################################################################

def _service_account_email() -> Optional[str]:
    try:
        with open(config.GOOGLE_SERVICE_ACCOUNT_FILE) as f:
            return json.load(f).get("client_email")
    except Exception:
        return None


def _get_service():
    if config.GOOGLE_CALENDAR_ID == "primary":
        raise RuntimeError(
            "GOOGLE_CALENDAR_ID is 'primary' but auth is a service account: "
            "events would land on an invisible calendar. Share your calendar "
            f"with {_service_account_email()} and set GOOGLE_CALENDAR_ID."
        )
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def _slot(iso: str) -> dict:
    return {"dateTime": datetime.fromisoformat(iso).isoformat(),
            "timeZone": config.GOOGLE_CALENDAR_TIMEZONE}


def _execute(request) -> str:
    try:
        r = request.execute()
    except HttpError as e:
        status = getattr(e.resp, "status", None)
        hint = ""
        if status in (403, 404):
            hint = (f" Share calendar with {_service_account_email()} "
                    "(permission: Make changes to events).")
        return json.dumps({"error": f"Calendar API {status}: {e}.{hint}"})
    return json.dumps({
        "id": r.get("id"),
        "htmlLink": r.get("htmlLink"),
        "summary": r.get("summary"),
        "start": r.get("start"),
        "end": r.get("end"),
    })


####################################################################################################
### PUBLIC TOOLS
####################################################################################################

def create_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    """Create a Google Calendar event. Datetimes are ISO 8601 strings."""
    body = {"summary": summary, "start": _slot(start_iso), "end": _slot(end_iso)}
    if description:
        body["description"] = description
    if location:
        body["location"] = location

    service = _get_service()
    request = service.events().insert(
        calendarId=config.GOOGLE_CALENDAR_ID, body=body
    )
    return _execute(request)


def update_event(
    event_id: str,
    summary: Optional[str] = None,
    start_iso: Optional[str] = None,
    end_iso: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    """Patch an existing event. Only the provided fields are touched."""
    body: dict = {}
    if summary is not None:
        body["summary"] = summary
    if description is not None:
        body["description"] = description
    if location is not None:
        body["location"] = location
    if start_iso is not None:
        body["start"] = _slot(start_iso)
    if end_iso is not None:
        body["end"] = _slot(end_iso)

    if not body:
        return json.dumps({"error": "no field to update"})

    service = _get_service()
    request = service.events().patch(
        calendarId=config.GOOGLE_CALENDAR_ID,
        eventId=event_id,
        body=body,
    )
    return _execute(request)
