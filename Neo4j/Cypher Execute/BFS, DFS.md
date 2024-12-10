# Dựng đồ thị trong Graph Catalog
```
CALL gds.graph.project(
  'Graph1', 
  'Node', 
  {
    CONNECTED: {
      type: 'CONNECTED', 
      properties: ['weight']
    }
  }
)
```

<hr>

# Chạy BFS ở chế độ stream
```
MATCH (source:Node {name: 'v1'})
CALL gds.bfs.stream('Graph1', {
  sourceNode: source
})
YIELD path
RETURN path
```

<hr>

# Chạy DFS ở chế độ stream
```
MATCH (source:Node{name:'v1'})
CALL gds.dfs.stream('Graph1', {
  sourceNode: source
})
YIELD path
RETURN path
```
