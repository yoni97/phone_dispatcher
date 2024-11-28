from flask import Blueprint, request, jsonify

from config.neo4j_config import neo4j_driver
from repository.phone_repo import query_neo4j
from services.phone_service import DeviceInteractions

phone_blueprint = Blueprint('phone_blueprint', __name__)

@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   data = request.get_json()
   try:
       repo = DeviceInteractions(neo4j_driver)
       new_device = repo.create_device(data)
       return jsonify({
            'status': 'success',
            'new_device': new_device
       }), 201
   except Exception as e:
       print(f'Error in POST /api/v1/transaction: {str(e)}')
       return jsonify({'error': 'internal server error'}), 500



@phone_blueprint.route('/bluetooth_connections', methods=['GET'])
def bluetooth_connections():
    query = """
    MATCH (a:Device)-[r:CONNECTED {method: 'Bluetooth'}]->(b:Device)
    RETURN a.id AS from_device, b.id AS to_device, r.duration_seconds AS duration
    """
    results = query_neo4j(query)
    return jsonify(results)

@phone_blueprint.route('/strong_signal', methods=['GET'])
def strong_signal():
    query = """
    MATCH (a:Device)-[r:CONNECTED]->(b:Device)
    WHERE r.signal_strength_dbm > -60
    RETURN a.id AS from_device, b.id AS to_device
    """
    results = query_neo4j(query)
    return jsonify(results)

@phone_blueprint.route('/connected_devices/<string:device_id>', methods=['GET'])
def connected_devices(device_id):
    query = """
    MATCH (:Device {id: $device_id})-[r:CONNECTED]->(b:Device)
    RETURN COUNT(b) AS connected_devices
    """
    results = query_neo4j(query, {"device_id": device_id})
    return jsonify(results)

@phone_blueprint.route('/is_connected', methods=['GET'])
def is_connected():
    from_device = request.args.get('from')
    to_device = request.args.get('to')
    query = """
    MATCH (a:Device {id: $from_device})-[r:CONNECTED]->(b:Device {id: $to_device})
    RETURN COUNT(r) > 0 AS is_connected
    """
    results = query_neo4j(query, {"from_device": from_device, "to_device": to_device})
    return jsonify(results[0])

@phone_blueprint.route('/recent_interaction/<string:device_id>', methods=['GET'])
def recent_interaction(device_id):
    query = """
    MATCH (:Device {id: $device_id})-[r:CONNECTED]->(b:Device)
    RETURN r ORDER BY r.timestamp DESC LIMIT 1
    """
    results = query_neo4j(query, {"device_id": device_id})
    return jsonify(results[0] if results else {})