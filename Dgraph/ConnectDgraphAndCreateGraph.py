import pydgraph
import networkx as nx
import matplotlib.pyplot as plt
import json

def create_dgraph_client():
    # Kết nối tới Dgraph (thay đổi endpoint nếu cần)
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

def set_schema(client):
    schema = """
    name: string @index(exact) .
    weight: int .
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)

def insert_data(client):
    # Dữ liệu đồ thị từ bảng
    edges = [
        ("v1", "v2", 4),
        ("v1", "v8", 8),
        ("v2", "v3", 8),
        ("v2", "v8", 11),
        ("v3", "v4", 7),
        ("v3", "v6", 4),
        ("v3", "v9", 2),
        ("v4", "v5", 9),
        ("v4", "v6", 14),
        ("v5", "v6", 10),
        ("v6", "v7", 2),
        ("v7", "v8", 1),
        ("v7", "v9", 6),
        ("v8", "v9", 7),
    ]

    # Chuẩn bị giao dịch
    txn = client.txn()
    try:
        for from_node, to_node, weight in edges:
            mutation = {
                "set": [
                    {"uid": f"_:{from_node}", "name": from_node},
                    {"uid": f"_:{to_node}", "name": to_node},
                    {"uid": f"_:{from_node}", "edges": [{"uid": f"_:{to_node}", "weight": weight}]}
                ]
            }
            txn.mutate(set_obj=mutation)
        txn.commit()
    finally:
        txn.discard()

def query_and_plot_graph(client):
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

    # Chuyển đổi dữ liệu truy vấn sang NetworkX
    G = nx.Graph()
    for node in data.get("graph", []):
        from_node = node["name"]
        for edge in node.get("edges", []):
            to_node = edge["name"]
            weight = edge["weight"]
            G.add_edge(from_node, to_node, weight=weight)

    # Vẽ đồ thị
    pos = nx.spring_layout(G)  # Bố trí đồ thị theo dạng lò xo
    plt.figure(figsize=(10, 8))

    # Vẽ các nút và cạnh
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="black")

    # Hiển thị trọng số cạnh
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Lưu đồ thị thành tệp hình ảnh
    plt.title("Đồ thị dựa trên dữ liệu từ Dgraph")
    plt.axis("off")
    plt.savefig("dgraph_output.png")
    plt.show()

def main():
    client, client_stub = create_dgraph_client()
    try:
        set_schema(client)
        insert_data(client)
        query_and_plot_graph(client)
    finally:
        client_stub.close()

if __name__ == "__main__":
    main()




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