import json

###WARNING _> should output text
def list_contacts():
    """"""
    return json.dumps([
        {
            "name": "Julien", 
            "phone": "+33695650878"
        },
        {
            "name": "Isaure", 
            "phone": "+33785626781"
        },
        # {
        #     "name": "jasper",
        #     "phone": "+33644355174" 
        # }
    ])