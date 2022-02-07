#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_list_places(city_id):
    """Retrieves the list of all Place objects of a City

    Args:
        city_id: Id of the City object to be gotten. Default to None.

    Raises:
        a: 404 error if the city_id is not linked to any City object

    Returns:
        [json string]: the list of all places of a city
    """
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    places = obj_city.places
    list_places = [place.to_dict() for place in places]
    return jsonify(list_places), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object

    Args:
        place_id: Id of the object to be gotten

    Raises:
        a: 404 error if the place_id is not linked to any Place object

    Returns:
        [json string]: a Place object
    """
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    return jsonify(obj_place.to_dict()), 200


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place object

    Arg:
        place_id: id of the object to be deleted

    Raises:
        a: 404 error if the place_id is not linked to any place object

    Returns:
        [Json string] an empty dictionary with the status code 200
    """
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    storage.delete(obj_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Creates a Place object

    Raises:
    a: 404 error if:
        - The city_id is not linked to any City object
        - The user_id is not linked to any User object
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "user_id".
            Message "Missing user_id"
        - The dictionary doesn’t contain the key "name".
            Message "Missing name"

    Returns:
        [json string]: The new Place with the status code 201
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    new_place_data = request.get_json()
    if new_place_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in new_place_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, new_place_data["user_id"])
    if user is None:
        abort(404)
    if "name" not in new_place_data.keys():
        abort(400, "Missing name")
    new_place_data['city_id'] = city.id
    new_place = Place(**new_place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Updates a Place object.
    Ignore keys: id, user_id, city_id, created_at and updated_at

    Args:
        place_id: Id of the object to be updated

    Raises:
        a: 404 error if:
            - The place_id is not linked to any Place object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"

    Returns:
        [json string]: The Place object with the status code 200
    """
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    new_place_data = request.get_json()
    if new_place_data is None:
        abort(400, "Not a JSON")
    for key, value in new_place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj_place, key, value)
    obj_place.save()
    return jsonify(obj_place.to_dict()), 200
