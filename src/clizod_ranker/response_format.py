SINGLE_LEVEL_QA_RESPONSE={
    "type": "json_schema",
    "json_schema": {
        "name": "question_n_answers",
        "schema": {
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_number": {
                                "type": "integer"
                            },
                            "reason": {
                                "type": "string"
                            },
                            "answer": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "question_number",
                            "reason",
                            "answer"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "results"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
} 

MULTI_LEVEL_QA_RESPONSE={
    "type": "json_schema",
    "json_schema": {
        "name": "question_n_answers",
        "schema": {
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_number": {
                                "type": "integer"
                            },
                            "reason": {
                                "type": "string"
                            },
                            "answer": {
                                "type": "string"
                            },
                            "confidence_score": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "question_number",
                            "reason",
                            "answer",
                            "confidence_score"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "results"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
} 
