from config.neo4j_config import neo4j_driver

def query_neo4j(cypher_query, parameters=None):
    with neo4j_driver.session() as session:
        return session.run(cypher_query, parameters).data()