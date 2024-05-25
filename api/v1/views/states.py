#!/usr/bin/python3
"""to retrieve an object into a valid JSON"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states/<string:id>')
@app_views.route('/states/')
def state_get(id=None):
    """CreateS a new view for State objects that handles 
    default RESTFul API actions
    """
    if id is None:
        print('1')
        states_list = []
        states = storage.all(State)
        for state in states.values():
            states_list.append(state.to_dict())
        return jsonify(states_list)
    
    else:
        print('2')
        state = storage.get(State, id)
        if state is None:
            print('3')
            abort(404)
        else:
            return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Method deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def create_state():
    states_dict = request.get_json()
    
    if states_dict is None:
        abort(400, 'Not a JSON')
    
    if 'name' not in states_dict.keys():
        abort(400, 'Missing name')
    
    new_state = State(**states_dict)
    storage.new(new_state)
    storage.save()
    
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    # Update the State object with the provided data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
