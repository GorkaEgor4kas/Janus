TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read a note by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to read.",
                    }
                },
                "required": ["note_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search notes by query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query.",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]