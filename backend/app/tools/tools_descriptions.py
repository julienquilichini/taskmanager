###

TOOLS_DESCRIPTIONS = [

    # 1. MAKE PHONE CALL
    {
        "type": "function",
        "function": {
            "name": "make_phone_call",
            "description": "Place an outbound phone call to a business or person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "description": "Phone number to call in E.164 format, e.g. +33123456789.",
                    },
                    "instructions": {
                        "type": "string",
                        "description": "What the assistant must accomplish during the call.",
                    },
                    "context": {
                        "type": "string",
                        "description": "Useful details for the call.",
                    },
                    # "greeting": {
                    #     "type": "string",
                    #     "description": "A short introduction sentence to begin the call",
                    # },
                },
                "required": ["phone_number", "instructions", "context"], # "greeting"],
            },
        },
    },

    # 2. LIST CONTACTS
    {
        "type": "function",
        "function": {
            "name": "list_contacts",
            "description": "Returns a list of the contacts",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [],
            },
        },
    },

    # 3. SEARCH WEB
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Returns the result of a web search for a given query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query you want to search the web about"
                    }
                },
                "required": ["query"],
            },
        },
    }

]