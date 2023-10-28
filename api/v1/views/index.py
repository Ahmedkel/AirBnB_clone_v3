#!/usr/bin/python3
"""running flask"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """return json status."""
    return jsonify({"status": "OK"})
