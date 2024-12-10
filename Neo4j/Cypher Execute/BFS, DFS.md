# Dựng đồ thị trong Graph Catalog
```
CALL gds.graph.project(
  'myGraph', 
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
CALL gds.bfs.stream('myGraph', {
  sourceNode: source
})
YIELD path
RETURN path
```

<hr>

# Chạy DFS ở chế độ stream
```
MATCH (source:Node{name:'A'})
CALL gds.dfs.stream('myGraph', {
  sourceNode: source
})
YIELD path
RETURN path
```
