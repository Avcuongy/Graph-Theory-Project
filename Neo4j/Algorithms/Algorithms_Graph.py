from collections import deque
import math
import heapq
import pandas as pd
import numpy as np


##==============================================================================
## Hàm duyệt đồ thị theo chiều RỘNG (Breadth First Searh - BFS)
##==============================================================================
def BFS(vertices, adj_df, vertex):
    # Chuẩn bị dữ liệu
    seq = []
    frees = pd.Series(1, index=vertices)  # Các đỉnh tự do
    queue = [vertex]  # Hàng đợi FIFO
    frees[vertex] = 0  # Đánh dấu đỉnh bắt đầu

    while queue:
        current = queue.pop(0)  # Lấy phần tử đầu tiên trong hàng đợi
        seq.append(current)

        # Xét các đỉnh kề
        for v in vertices:
            if adj_df.loc[current, v] != math.inf and frees[v] == 1:
                queue.append(v)
                frees[v] = 0  # Đánh dấu đã thăm

    return seq


##==============================================================================
## Hàm duyệt đồ thị theo chiều RỘNG, có lưu vết thứ tự duyệt đỉnh
##==============================================================================
def BFS_path(vertices, adj_df, vertex):
    seq = []  # Thứ tự các đỉnh được duyệt
    preds = pd.Series(None, index=vertices)  # Đỉnh trước của mỗi đỉnh
    frees = pd.Series(1, index=vertices)  # Các đỉnh tự do
    queue = [vertex]  # Hàng đợi FIFO
    frees[vertex] = 0  # Đánh dấu đỉnh bắt đầu

    while queue:
        current = queue.pop(0)  # Lấy phần tử đầu tiên
        seq.append(current)

        # Xét các đỉnh kề
        for v in vertices:
            if adj_df.loc[current, v] != math.inf and frees[v] == 1:
                if pd.isna(preds[v]):
                    preds[v] = current  # Lưu vết đỉnh trước
                queue.append(v)
                frees[v] = 0  # Đánh dấu đã thăm

    return seq, preds


##==============================================================================
## Hàm xác định thành phần liên thông với đỉnh [vertex] dựa trên BFS
##==============================================================================
def BFS_component(vertices, adj_df, vertex):
    return BFS(vertices, adj_df, vertex)


##==============================================================================
## Hàm xác định TẤT CẢ các thành phần liên thông của đồ thị dựa trên BFS
##==============================================================================
def BFS_all_components(vertices, adj_df):
    components = []  # Danh sách chứa các thành phần liên thông
    unvisited = set(vertices)  # Tập hợp các đỉnh chưa được duyệt

    while unvisited:
        # Lấy một đỉnh bất kỳ trong tập hợp đỉnh chưa duyệt
        start_vertex = unvisited.pop()

        # Tìm thành phần liên thông chứa đỉnh đó bằng BFS
        component = BFS(vertices, adj_df, start_vertex)

        # Thêm thành phần liên thông vào danh sách
        components.append(component)

        # Loại bỏ các đỉnh thuộc thành phần liên thông ra khỏi tập hợp chưa duyệt
        unvisited -= set(component)

    return components


##==============================================================================
## Thủ tục đệ quy duyệt đồ thị theo chiều SÂU (Depth First Searh - DFS)
##==============================================================================
def DFS(vertices, adj_df, frees, vertex, seq):
    # Đánh dấu đỉnh hiện tại là đã thăm
    frees[vertex] = 0
    seq.append(vertex)

    # Duyệt qua các đỉnh láng giềng kề với đỉnh hiện tại
    for v in vertices:
        if adj_df.loc[vertex, v] != math.inf and frees[v] == 1:
            DFS(vertices, adj_df, frees, v, seq)


##==============================================================================
## Hàm xác định thành phần liên thông với đỉnh [vertex] dựa trên DFS
##==============================================================================
def DFS_component(vertices, adj_df, vertex):
    # Khởi tạo trạng thái tự do
    frees = pd.Series(1, index=vertices)
    seq = []

    # Bắt đầu duyệt từ đỉnh được chọn
    DFS(vertices, adj_df, frees, vertex, seq)

    return seq


##==============================================================================
## Hàm xác định TẤT CẢ các thành phần liên thông của đồ thị dựa trên DFS
##==============================================================================
def DFS_all_components(vertices, adj_df):
    components = []
    vertices = list(vertices)

    while vertices:
        # Lấy thành phần liên thông đầu tiên
        component = DFS_component(vertices, adj_df, vertices[0])
        components.append(component)

        # Loại bỏ các đỉnh đã thuộc thành phần liên thông
        vertices = list(set(vertices) - set(component))

    return components


##==============================================================================
## Thủ tục đệ quy DFS, có lưu vết thứ tự duyệt đỉnh
##==============================================================================
def DFS_path(vertices, adj_df, frees, vertex, seq, pred_ser):
    # vertices: các đỉnh (series)
    # adj_df  : ma trận kề (dataframe)
    # frees   : trạng thái tự do (= 1) hay không (= 0) của các đỉnh (series)
    # vertex  : đỉnh đang xét duyệt (label: string)
    # seq     : chuỗi thứ tự các đỉnh được duyệt
    # preds   : đỉnh duyệt trước của các đỉnh đã duyệt (series)
    # ---------------------------------------------------------------------------
    # Duyệt những đỉnh tự do và kề với đỉnh [vertex]
    # Đánh dấu đỉnh hiện tại là đã thăm
    frees[vertex] = 0
    seq.append(vertex)

    # Duyệt qua các đỉnh kề tự do của đỉnh hiện tại
    for v in vertices:
        if adj_df.loc[vertex, v] != math.inf and frees[v] == 1:
            if pd.isna(pred_ser[v]):  # Nếu chưa lưu predecessor, thì lưu
                pred_ser[v] = vertex

            # Đệ quy duyệt tiếp
            DFS_path(vertices, adj_df, frees, v, seq, pred_ser)


# Bellman-Ford
def bellman_ford(df_matrix, start):
    nodes = df_matrix.index
    dist = {node: float("inf") for node in nodes}
    dist[start] = 0

    edges = []
    for u in nodes:
        for v in nodes:
            if df_matrix.at[u, v] != np.inf and u != v:
                edges.append((u, v, df_matrix.at[u, v]))

    for _ in range(len(nodes) - 1):
        for u, v, weight in edges:
            if dist[u] != float("inf") and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight

    for u, v, weight in edges:
        if dist[u] != float("inf") and dist[u] + weight < dist[v]:
            return None

    return dist


# Dijkstra
def dijkstra(df_matrix, start):
    nodes = df_matrix.index
    dist = {node: float("inf") for node in nodes}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        neighbors = df_matrix.loc[node][df_matrix.loc[node] > 0]
        for neighbor, weight in neighbors.items():
            distance = current_dist + weight

            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return dist


# Prim
def prim(adj_matrix):
    vertices = adj_matrix.index.tolist()
    num_vertices = len(vertices)

    selected_nodes = [False] * num_vertices
    mst_edges = []
    min_edge = [np.inf] * num_vertices
    parent = [-1] * num_vertices

    min_edge[0] = 0

    for _ in range(num_vertices):
        u = np.argmin(min_edge)
        selected_nodes[u] = True

        if parent[u] != -1:
            mst_edges.append(
                (vertices[parent[u]], vertices[u], adj_matrix.iloc[parent[u], u])
            )

        for v in range(num_vertices):
            if not selected_nodes[v] and adj_matrix.iloc[u, v] < min_edge[v]:
                min_edge[v] = adj_matrix.iloc[u, v]
                parent[v] = u

        min_edge[u] = np.inf

    return mst_edges


# Kruskal
def kruskal(df):
    edges = df.sort_values("Weight").values.tolist()
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    for node in set(df["From"]).union(df["To"]):
        parent[node] = node
        rank[node] = 0

    mst = []
    total_weight = 0

    for edge in edges:
        u, v, weight = edge
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))
            total_weight += weight

    return mst, total_weight


# Sequential Coloring
def sequential_coloring(adj_matrix):
    vertices = adj_matrix.index.tolist()
    degree = adj_matrix.sum(axis=1).sort_values(ascending=False)
    vertices_order = degree.index.tolist()

    colors = {v: None for v in vertices}

    for vertex in vertices_order:
        neighbor_colors = set(
            colors[neighbor]
            for neighbor in adj_matrix.columns[adj_matrix.loc[vertex] == 1]
            if colors[neighbor] is not None
        )

        color = 0
        while color in neighbor_colors:
            color += 1

        colors[vertex] = color

    return colors
