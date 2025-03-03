import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datastructures import FamilyStructure
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/members", methods=["GET"])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route("/member", methods=["POST"])
def post_member():
    member = request.json
    if not all(key in member for key in ["first_name", "age", "lucky_numbers"]):
        return jsonify({"error": "Invalid input"}), 400
    new_member = jackson_family.add_member(member)
    return jsonify(new_member), 200

@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
