from collections import deque
import heapq
import pandas as pd
import numpy as np


# BFS
def bfs(df_matrix, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        neighbors = df_matrix.loc[node][df_matrix.loc[node] < np.inf].index
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


# DFS
def dfs(df_matrix, start):
    visited = set()
    result = []

    def dfs_recursive(node):
        visited.add(node)
        result.append(node)

        neighbors = df_matrix.loc[node][df_matrix.loc[node] < np.inf].index
        for neighbor in neighbors:
            if neighbor not in visited:
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return result


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
