from config.neo4j_config import neo4j_driver

def query_neo4j(cypher_query, parameters=None):
    with neo4j_driver.session() as session:
        return session.run(cypher_query, parameters).data()

def get_bluetooth_connections():
    query = """
    MATCH (start:Device)
    MATCH (end:Device)
    WHERE start <> end
    MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
    WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
    WITH path, length(path) as pathLength
    ORDER BY pathLength DESC
    LIMIT 1
    RETURN length(path)
    """
    results = query_neo4j(query)
    if not results:
        return []
    return results

def get_strong_signal():
    query = """
        MATCH (a:Device)-[r:CONNECTED]->(b:Device)
        WHERE r.signal_strength_dbm > -60
        RETURN a.id AS from_device, b.id AS to_device, r.signal_strength_dbm 
        """
    result = query_neo4j(query)
    if not result:
        return []
    return result

def get_connected_devices(id):
    query = """
        MATCH (:Device {id: $id})-[r:CONNECTED]->(b:Device)
        RETURN COUNT(b) AS connected_devices
        """
    result = query_neo4j(query, {"id": id})
    if not result:
        return []
    return result

def get_connections(from_device, to_device):
    query = """
            MATCH (d1:Device)-[r:CONNECTED]-(d2:Device)
            WHERE d1.id = $from_device AND d2.id = $to_device
            RETURN COUNT(r) > 0 AS is_connected
        """
    result = query_neo4j(query, {"from_device": from_device, "to_device": to_device})
    if not result:
        return []
    return result

def get_last_connection(id):
    query = """
        MATCH (a:Device {id: $id})-[r:CONNECTED]->(b:Device)
        RETURN a.id AS FROM_DEVICE, b.id AS TO_DEVICE,
        r.timestamp AS timestamp
        ORDER BY r.timestamp DESC 
        LIMIT 1
        """
    result = query_neo4j(query, {"id": id})
    return result