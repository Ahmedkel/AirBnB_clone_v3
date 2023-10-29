#!/usr/bin/python3
"""running flask"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def status():
    """return json status."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """return json status."""
    return jsonify({
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
        })
