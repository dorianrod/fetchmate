import os
from config import app
from flask import jsonify


@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "version": os.getenv("VERSION")})
