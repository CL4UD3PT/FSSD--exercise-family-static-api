"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all_members():
    members = jackson_family.get_all_members()
    if not len(members) > 0:
        return jsonify({"Members": "No members found"}), 404
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return("No member found with this id"), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def handle_new_member():
    response = jackson_family.add_member(request.json)
    if not response:
        return jsonify("Something went wrong. Please check your data."), 400
    return jsonify({"Members":"Member added successfully!"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    response = jackson_family.delete_member(id)
    if not response:
        return jsonify(response), 400
    return jsonify(response), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
