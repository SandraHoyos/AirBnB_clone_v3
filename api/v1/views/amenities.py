#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id=None):
    """Retrieves the list of all Amenity objects if amenity_id is None, if not,
    retrieves an Amenity object

    Args:
        amenity_id: Id of the object to be gotten. Defaults to None.

    Raises:
        a: 404 error if the amenity_id is not linked to any Amenity object
    Returns:
        [json string]: The list of all Amenity objects if amenity_id is None,
        if not, retrieves an Amenity object
    """
    if amenity_id is None:
        list_obj_amenity = storage.all(Amenity).values()
        dict_obj_amenity = [obj.to_dict() for obj in list_obj_amenity]
        return jsonify(dict_obj_amenity), 200
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    return jsonify(obj_amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object

    Args:
        amenity_id: Id of the object to be deleted

    Raises:
        a: 404 error if the amenity_id is not linked to any amenity object

    Returns:
        [json string]: An empty dictionary with the status code 200
    """
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    storage.delete(obj_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates an Amenity object

    Raises:
    a: 400 error if:
        - The HTTP body request is not valid JSON. Message "Not a JSON"
        - The dictionary doesn’t contain the key "name". Message "Missing name"

    Returns:
        [json string]: The new Amenity with the status code 201
    """
    new_amenity_data = request.get_json()
    if new_amenity_data is None:
        abort(400, "Not a JSON")
    if "name" not in new_amenity_data.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**new_amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity object.
    Ignore keys: id, created_at and updated_at

    Args:
        amenity_id: Id of the object to be updated
    Raises:
        a: 404 error if:
            - The amenity_id is not linked to any Amenity object.
        a: 400 error if:
            - The HTTP body request is not valid JSON. Message "Not a JSON"
    Returns:
        [json string]: The Amenity object with the status code 200
    """
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    new_amenity_data = request.get_json()
    if new_amenity_data is None:
        abort(400, "Not a JSON")
    for key, value in new_amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj_amenity, key, value)
    obj_amenity.save()
    return jsonify(obj_amenity.to_dict()), 200
