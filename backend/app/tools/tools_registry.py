###
from app.tools.make_phone_call import make_phone_call
from app.tools.list_contacts import list_contacts
from app.tools.web_search import search_web

TOOLS_REGISTRY = {

    "make_phone_call": make_phone_call,

    "list_contacts": list_contacts,

    "search_web": search_web,

    # "send_telegram": send_telegram,

}