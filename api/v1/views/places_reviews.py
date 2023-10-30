#!/usr/bin/python3
"""running flask"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Get all reviews of a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a specific review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a specific review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a specific review."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
