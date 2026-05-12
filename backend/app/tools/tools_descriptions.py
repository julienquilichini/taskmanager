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
    },

    # 4. CREATE CALENDAR EVENT
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a new event on the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Title of the event.",
                    },
                    "start_iso": {
                        "type": "string",
                        "description": "Event start in ISO 8601, e.g. 2026-05-12T14:30:00.",
                    },
                    "end_iso": {
                        "type": "string",
                        "description": "Event end in ISO 8601, e.g. 2026-05-12T15:00:00.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional event description / notes.",
                    },
                    "location": {
                        "type": "string",
                        "description": "Optional event location.",
                    },
                },
                "required": ["summary", "start_iso", "end_iso"],
            },
        },
    },

    # 5. UPDATE CALENDAR EVENT
    {
        "type": "function",
        "function": {
            "name": "update_calendar_event",
            "description": "Update fields of an existing Google Calendar event. Only the provided fields are changed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "ID of the event to update (returned by create_calendar_event).",
                    },
                    "summary": {
                        "type": "string",
                        "description": "New title.",
                    },
                    "start_iso": {
                        "type": "string",
                        "description": "New start datetime in ISO 8601.",
                    },
                    "end_iso": {
                        "type": "string",
                        "description": "New end datetime in ISO 8601.",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description.",
                    },
                    "location": {
                        "type": "string",
                        "description": "New location.",
                    },
                },
                "required": ["event_id"],
            },
        },
    },

]