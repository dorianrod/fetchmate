import hashlib
import json
import logging
import os
import time
from config import app
from flask import jsonify, request
from jsonschema import validate, ValidationError

from utils.openai import ask_chatgpt
from services.build_prompt.build_context_prompt import build_context_prompt
from .validation_schema import schema
from config import cache


def get_data_from_request(request):
    try:
        return request.get_json()
    except Exception:
        data_str = request.data.decode('utf-8')
        data_str = data_str.strip("b'")
        data_json = json.loads(data_str)
        return data_json


def generate_cache_key():
    json_data = get_data_from_request(request)
    stringified_json = json.dumps(json_data, sort_keys=True)
    return hashlib.sha256(stringified_json.encode()).hexdigest()


@app.route('/query', methods=['POST'])
@cache.cached(
    timeout=int(os.getenv("CACHE_IN_DURATION", 3600)),
    key_prefix=generate_cache_key,
)
def query_api():
    data = request.get_json()

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    role, messages = build_context_prompt(data)
    try:
        debug_response = get_debug_response(data, role, messages)
        if debug_response:
            return debug_response

        response, usage = ask_chatgpt(role, messages)
        status = "OK" if "SELECT" in response else "HELP"

        return jsonify(
            {
                "status": status,
                "response": response,
                "usage": usage,
                "prompt": [role, *messages],
            }
        )

    except Exception as e:
        logging.exception(e)
        return jsonify({"status": "ERROR", "message": str(e)}), 500


def get_debug_response(data, role, messages):
    is_debug = int(os.getenv("DEBUG_RESPONSE", "0"))
    if is_debug == 0:
        return

    base_reponse = {
        "engine": data["engine"],
        "status": "OK",
        "usage": {
            "completion_tokens": 63,
            "prompt_tokens": 693,
            "total_tokens": 756,
        },
    }

    time.sleep(1)

    if "template" in data["prompt"]:
        return jsonify(
            {
                "response": json.dumps(role) + " - " + json.dumps(messages),
                **base_reponse,
            }
        )

    if "input" in data["prompt"]:
        return jsonify({"response": json.dumps(data), **base_reponse})

    if "help" in data["prompt"]:
        return jsonify(
            {
                "response": "You are required to provide additional details in order for me to assist you effectively.",
                **base_reponse,
                "status": "HELP",
            }
        )

    return jsonify(
        {
            "response": data["prompt"],
            **base_reponse,
        }
    )
