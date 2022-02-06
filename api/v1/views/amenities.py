#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import models
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states(state_id=None):
    """Retrieves the list of all State objects if state_id is None, if not
    retrieves a State object
    Args:
        state_id: Id of the object to be gotten. Defaults to None.
    Raises:
        a: 404 error if the state_id is not linked to any State object
    Returns:
        [json string]: The list of all State objects if state_id is None,
        if not
    retrieves a State object
    """
    if state_id is None:
        list_obj_state = models.storage.all(State).values()
        dict_obj_state = [obj.to_dict() for obj in list_obj_state]
        return jsonify(dict_obj_state), 200
    obj_state = models.storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    return jsonify(obj_state.to_dict()), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object
    Args:
        state_id: Id of the object to be deleted
    Raises:
        a: 404 error if the state_id is not linked to any State object
    Returns:
        [json string]: An empty dictionary with the status code 200
    """
    obj_state = models.storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    models.storage.delete(obj_state)
    models.storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State object
    Raises:
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "name". Message "Missing name"
    Returns:
        [json string]: The new State with the status code 201
    """
    new_state_data = request.get_json()
    if new_state_data is None:
        abort(400, "Not a JSON")
    if "name" not in new_state_data.keys():
        abort(400, "Missing name")
    new_state = State(**new_state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a state object.
    Ignore keys: id, created_at and updated_at
    Args:
        state_id: Id of the object to be updated
    Raises:
        a: 404 error if:
            - The state_id is not linked to any State object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"
    Returns:
        [json string]: The State object with the status code 200
    """
    obj_state = models.storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    new_state_data = request.get_json()
    if new_state_data is None:
        abort(400, "Not a JSON")
    for key, value in new_state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj_state, key, value)
    obj_state.save()
    return jsonify(obj_state.to_dict()), 200