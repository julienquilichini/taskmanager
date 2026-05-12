###
from app.tools.make_phone_call import make_phone_call
from app.tools.list_contacts import list_contacts
from app.tools.web_search import search_web
from app.tools.update_calendar import create_event, update_event

TOOLS_REGISTRY = {

    "make_phone_call": make_phone_call,

    "list_contacts": list_contacts,

    "search_web": search_web,

    "create_calendar_event": create_event,

    "update_calendar_event": update_event,

    # "send_telegram": send_telegram,

}