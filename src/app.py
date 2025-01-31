"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({'id': 335,'first_name':'John', 
                          'last_name': jackson_family.last_name,'age': 33,
                          'lucky_numbers': [7,13,22]})
jackson_family.add_member( {'id': 336,'first_name':'Jane', 
                          'last_name': jackson_family.last_name,'age': 35,
                          'lucky_numbers': [10,14,3]})
jackson_family.add_member( {'id': 337,'first_name':'Jimmy', 
                          'last_name': jackson_family.last_name,'age': 5,
                          'lucky_numbers': [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_start():
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        if not members:
            return jsonify('Bad request'), 400
        response_body = {
            "hello": "world",
            "family": members
        }
        return jsonify(response_body['family']), 200
    except Exception as e:
        return jsonify('Internal server error'), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def handle_get_member(member_id):
    try:
        response_body = jackson_family.get_member(member_id)
        if response_body is None:
            return jsonify('Bad request: member not found'),400
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify('Internal server error'), 500

@app.route('/member', methods=['POST'])
def handle_add_member():
    try:
        request_body = request.get_json(force=True)
        response_body = jackson_family.add_member(request_body)
        if response_body is None:
            return jsonify('Bad request: request is missing properties or includes invalid data types'), 400
        return jsonify(response_body), 200
    except BadRequest as e:
        return jsonify('Bad request: request is not JSON'), 400
    except Exception as e:
        return jsonify('Internal server error'), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    try:
        response = jackson_family.delete_member(member_id)
        if response is None:
            return jsonify('Bad request: member not found'), 400
        response_body = {'done':True}
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify('Internal server error'), 500
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
