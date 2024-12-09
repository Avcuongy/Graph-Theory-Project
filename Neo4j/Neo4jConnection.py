from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, password):
        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            raise

    def close(self):
        if self._driver:
            self._driver.close()

    def query(self, query, parameters=None):
        try:
            with self._driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
