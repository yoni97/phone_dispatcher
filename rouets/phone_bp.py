from flask import Blueprint, request, jsonify

from repository.phone_repo import query_neo4j

phone_blueprint = Blueprint('phone_blueprint', __name__)

@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200

