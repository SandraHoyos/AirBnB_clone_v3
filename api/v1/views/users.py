#!/usr/bin/python3
"""View for User objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id=None):
    """Retrieves the list of all User objects if user_id is None, if not then
    retrieves a User object

    Args:
        user_id: Id of the object to be gotten. Defaults to None.

    Raises:
        a: 404 error if the user_id is not linked to any User object
    Returns:
        [json string]: The list of all User objects if user_id is None,
        if not then retrieves a User object
    """
    if user_id is None:
        list_obj_user = storage.all(User).values()
        dict_obj_user = [obj.to_dict() for obj in list_obj_user]
        return jsonify(dict_obj_user), 200
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    return jsonify(obj_user.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object

    Args:
        user_id: Id of the object to be deleted

    Raises:
        a: 404 error if the user_id is not linked to any User object

    Returns:
        [json string]: An empty dictionary with the status code 200
    """
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    storage.delete(obj_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a User object

    Raises:
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "email".
            Message "Missing email"
        - The dictionary doesn’t contain the key "password".
            Message "Missing password"

    Returns:
        [json string]: The new user with the status code 201
    """
    new_user_data = request.get_json()
    if new_user_data is None:
        abort(400, "Not a JSON")
    if "email" not in new_user_data.keys():
        abort(400, "Missing email")
    if "password" not in new_user_data.keys():
        abort(400, "Missing password")
    new_user = User(**new_user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates a User object.
    Ignore keys: id, email, created_at and updated_at

    Args:
        user_id: Id of the object to be updated
    Raises:
        a: 404 error if:
            - The user_id is not linked to any user object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"
    Returns:
        [json string]: The User object with the status code 200
    """
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    new_user_data = request.get_json()
    if new_user_data is None:
        abort(400, "Not a JSON")
    for key, value in new_user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj_user, key, value)
    obj_user.save()
    return jsonify(obj_user.to_dict()), 200
