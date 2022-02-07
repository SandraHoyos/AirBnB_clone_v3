#!/usr/bin/python3
"""View for Review objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_list_reviews(place_id):
    """Retrieves the list of all Review objects of a Place

    Args:
        place_id: Id of the Place object to be gotten

    Raises:
        a: 404 error if the place_id is not linked to any Place object

    Returns:
        [json string]: the list of all Review objects of a Place
    """
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    reviews = obj_place.reviews
    list_reviews = [review.to_dict() for review in reviews]
    return jsonify(list_reviews), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object

    Args:
        review_id: Id of the object to be gotten

    Raises:
        a: 404 error if the review_id is not linked to any Review object

    Returns:
        [json string]: a Review object
    """
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    return jsonify(obj_review.to_dict()), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object

    Arg:
        review_id: id of the object to be deleted

    Raises:
        a: 404 error if the review_id is not linked to any Review object

    Returns:
        [Json string] an empty dictionary with the status code 200
    """
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    storage.delete(obj_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Creates a Review object

    Raises:
    a: 404 error if:
        - The place_id is not linked to any Place object
        - The user_id is not linked to any User object
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "user_id".
            Message "Missing user_id"
        - The dictionary doesn’t contain the key "text".
            Message "Missing text"

    Returns:
        [json string]: The new Review with the status code 201
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_review_data = request.get_json()
    if new_review_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in new_review_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, new_review_data["user_id"])
    if user is None:
        abort(404)
    if "text" not in new_review_data.keys():
        abort(400, "Missing text")
    new_review_data['place_id'] = place.id
    new_review = Review(**new_review_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Updates a Review object.
    Ignore keys: id, user_id, place_id, created_at and updated_at

    Args:
        review_id: Id of the object to be updated

    Raises:
        a: 404 error if:
            - The review_id is not linked to any Review object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"

    Returns:
        [json string]: The Review object with the status code 200
    """
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    new_review_data = request.get_json()
    if new_review_data is None:
        abort(400, "Not a JSON")
    for key, value in new_review_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(obj_review, key, value)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 200
