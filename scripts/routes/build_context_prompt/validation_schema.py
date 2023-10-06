schema = {
    "type": "object",
    "properties": {
        "engine": {"type": "string", "minLength": 1},
        "prompts": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "context": {"type": "string", "minLength": 1},
        "tables": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "minLength": 1},
                                "description": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    },
                },
                "required": ["name"],
            },
        },
    },
    "required": ["tables", "prompts", "engine"],
}
