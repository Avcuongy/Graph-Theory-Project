import pydgraph
import networkx as nx
import json

def create_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

def query_graph_data(client):
    query = """
    {
        graph(func: has(name)) {
            uid
            name
            edges {
                name
                weight
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    data = json.loads(response.json.decode('utf-8'))
    return data.get("graph", [])

def build_graph(data):
    G = nx.Graph()
    for node in data:
        from_node = node["name"]
        for edge in node.get("edges", []):
            to_node = edge["name"]
            weight = edge["weight"]
            G.add_edge(from_node, to_node, weight=weight)
    return G

def dijkstra_shortest_path(graph, start_node):
    # Thuật toán Dijkstra tìm đường đi ngắn nhất từ đỉnh bắt đầu đến các đỉnh còn lại.
    lengths, paths = nx.single_source_dijkstra(graph, start_node)
    
    print(f"Shortest path from {start_node}:")
    for target, length in lengths.items():
        print(f"To {target}: {length} (Path: {paths[target]})")

def query_and_dijkstra(client, start_node):
    # Truy vấn dữ liệu đồ thị từ Dgraph
    graph_data = query_graph_data(client)
    
    # Xây dựng đồ thị NetworkX từ dữ liệu Dgraph
    G = build_graph(graph_data)
    
    # Tìm đường đi ngắn nhất từ start_node sử dụng thuật toán Dijkstra
    dijkstra_shortest_path(G, start_node)

def main():
    client, client_stub = create_dgraph_client()
    try:
        # Thực hiện Dijkstra từ một đỉnh bắt đầu, ví dụ: 'v1'
        start_node = 'v1'
        query_and_dijkstra(client, start_node)
    finally:
        client_stub.close()

if __name__ == "__main__":
    main()
