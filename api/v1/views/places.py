#!/usr/bin/python3
"""Places objects that handles all default RestFul API actions"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_dict = request.get_json()
    if place_dict is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in place_dict.keys():
        abort(400, 'Missing user_id')
    if 'name' not in place_dict.keys():
        abort(400, 'Missing name')
    user = storage.get(User, place_dict['user_id'])
    if user is None:
        abort(404)
    place_dict['city_id'] = city_id
    new_place = Place(**place_dict)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_dict = request.get_json()
    if place_dict is None:
        abort(400, 'Not a JSON')
    for key, value in place_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the JSON in the request body"""
    search_data = request.get_json()
    if not search_data:
        abort(400, 'Not a JSON')
    
    # Query all places
    all_places = storage.all(Place).values()

    # Filter places based on search data
    filtered_places = []
    for place in all_places:
        if all(getattr(place, key, None) == value for key, value in search_data.items()):
            filtered_places.append(place.to_dict())

    return jsonify(filtered_places)
# def search_place(place_dict):
#     """Search a Place"""
#     places_list = []
#     places = storage.all(Place).values()
#     for place in places:
#         for key, value in place_dict.items():
#             if key == 'amenities':
#                 if all(amenity in place.amenities for amenity in value):
#                     places_list.append(place.to_dict())
#             elif key == 'name':
#                 if value in place.name:
#                     places_list.append(place.to_dict())
#             elif key == 'city_id':
#                 if value == place.city_id:
#                     places_list.append(place.to_dict())
#             elif key == 'user_id':
#                 if value == place.user_id:
#                     places_list.append(place.to_dict())
#     return places_list


if __name__ == '__main__':
    pass
