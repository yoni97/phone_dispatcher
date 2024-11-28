from flask import Blueprint, request, jsonify
from config.neo4j_config import neo4j_driver
from repository.phone_repo import get_bluetooth_connections, get_strong_signal, get_connected_devices, \
    get_last_connection, get_connections
from services.phone_service import DeviceInteractions

phone_blueprint = Blueprint('phone_blueprint', __name__)

@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   data = request.get_json()
   print(data)
   if not data or 'devices' not in data or 'interaction' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

   try:
       repo = DeviceInteractions(neo4j_driver)
       new_device = repo.create_device(data)
       return jsonify({
            'status': 'success'
       }), 201
   except Exception as e:
       print(f'Error in POST /api/phone_tracker: {str(e)}')
       return jsonify({'error': 'internal server error'}), 500

@phone_blueprint.route('/bluetooth_connections', methods=['GET'])
def bluetooth_connections():
    result = get_bluetooth_connections()
    return jsonify(result)

@phone_blueprint.route('/strong_signal', methods=['GET'])
def strong_signal():
    result = get_strong_signal()
    return jsonify(result)

@phone_blueprint.route('/connected_devices/<string:id>', methods=['GET'])
def connected_devices(id):
    results = get_connected_devices(id)
    return jsonify(results)

@phone_blueprint.route('/is_connected', methods=['GET'])
def is_connected():
    from_device = request.args.get('from')
    print(from_device)
    to_device = request.args.get('to')
    print(to_device)
    results = get_connections(from_device, to_device)
    return jsonify(results[0])

@phone_blueprint.route('/last_connection/<string:id>', methods=['GET'])
def last_connection(id):
    results = get_last_connection(id)

    if results:
        results[0]['timestamp'] = results[0]['timestamp'].isoformat()

    return jsonify(results[0] if results else {})