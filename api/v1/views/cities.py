#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_list_cities(state_id):
    """Retrieves the list of all City objects of a State

    Args:
        state_id: Id of the State object to be gotten. Default to None.

    Raises:
        a: 404 error if the state_id is not linked to any State object

    Returns:
        [json string]: the list of all cities of a state
    """
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    cities = obj_state.cities
    list_cities = [city.to_dict() for city in cities]
    return jsonify(list_cities), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a City object

    Args:
        city_id: Id of the object to be gotten

    Raises:
        a: 404 error if the city_id is not linked to any City object

    Returns:
        [json string]: a City object
    """
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    return jsonify(obj_city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object

    Arg:
        city_id: id of the object to be deleted

    Raises:
        a: 404 error if the city is not linked to any city object

    Returns:
        [Json string] an empty dictionary with the status code 200
    """
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    storage.delete(obj_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Creates a City object

    Raises:
    a: 404 error if the state_id is not linked to any State object
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "name". Message "Missing name"

    Returns:
        [json string]: The new City with the status code 201
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_city_data = request.get_json()
    if new_city_data is None:
        abort(400, "Not a JSON")
    if "name" not in new_city_data.keys():
        abort(400, "Missing name")
    new_city_data['state_id'] = state.id
    new_city = City(**new_city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a city object.
    Ignore keys: id, state_id, created_at and updated_at

    Args:
        city_id: Id of the object to be updated

    Raises:
        a: 404 error if:
            - The city_id is not linked to any city object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"

    Returns:
        [json string]: The city object with the status code 200
    """
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    new_city_data = request.get_json()
    if new_city_data is None:
        abort(400, "Not a JSON")
    for key, value in new_city_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj_city, key, value)
    obj_city.save()
    return jsonify(obj_city.to_dict()), 200
