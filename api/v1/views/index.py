#!/usr/bin/python3
"""File doc"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Return a JSON response indicating the status of the server."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Return a JSON response containing the number of objects by type."""
    from models import storage
    stats_json = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats_json)
