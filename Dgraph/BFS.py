import pydgraph
import networkx as nx
import matplotlib.pyplot as plt
import json
from collections import deque

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

def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    while queue:
        node = queue.popleft()
        print(f"Visiting node: {node}")
        
        # Thêm các đỉnh chưa được thăm vào hàng đợi
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def query_and_bfs(client, start_node):
    # Truy vấn dữ liệu đồ thị từ Dgraph
    graph_data = query_graph_data(client)
    
    # Xây dựng đồ thị NetworkX từ dữ liệu Dgraph
    G = build_graph(graph_data)
    
    # Thực hiện BFS từ start_node
    print(f"Starting BFS from node: {start_node}")
    bfs(G, start_node)

def main():
    client, client_stub = create_dgraph_client()
    try:
        # Thực hiện BFS từ một đỉnh bắt đầu, ví dụ: 'v1'
        start_node = 'v1'
        query_and_bfs(client, start_node)
    finally:
        client_stub.close()

if __name__ == "__main__":
    main()
