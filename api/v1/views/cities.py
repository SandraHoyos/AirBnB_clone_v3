#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
import models
from models import city



@app_views.route('/states/<state_id>/cities', strict_slashes=False, methodos=['GET'])
def cities(city_id=None):
    """Retrieves the list of all City objects of a State
    
    Args:
        city_id: Id of the object to be gotten. Default to None.
        
    Raises:
        a: 404 error if the city_id is not linked to any cities object
        
    Returns:
        [Jjon string]: the list of all cities objects if cities_id is None,
    retrieves a city object
    """

    if city_id is None:
        list_obj_city = models.storage.all(city).values()
        dict_obj_city = [obj.to_dict() for obj in list_obj_city]
        return jsonify(dict_obj_city), 200
    obj_city = models.storage.get(city, city_id)
    if obj_city is None:
        abort(404)
    return jsonify(obj_city.to_dict()), 200

@app_views.route('/states/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object
    
    Arg:
        city_id: id of the object to be deleted
        
    Raises:
        a: 404 error if the city is not linked to any city object
        
    Returns:
        [Jjon string] an empty dictionary with the status code 200
    """

    obj_city = models.storage.get(city, city:id)
    if obj_city is None:
        abort(404)
    models.storage.delete(obj_city)
    models. storage.save()
    return jsonify({}), 200

@app_views.route('states', strict_slashes=False, methods=['POST'])
def create_city():
    """create a new city
    
    Raises:
    a: 400 error if:
        - The HTTP body request is not valid JSON. message "NOt a JSON"
        - The dictionary doesn't contain the key "name". Message "missing name"
    
    Returns:
         [Jjon string]: The new state with the status code 201
        """




