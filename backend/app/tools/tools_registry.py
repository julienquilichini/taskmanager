###
from app.tools.make_phone_call import make_phone_call
from app.tools.list_contacts import list_contacts

TOOLS_REGISTRY = {

    "make_phone_call": make_phone_call,

    "list_contacts": list_contacts

}