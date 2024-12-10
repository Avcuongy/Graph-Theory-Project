# Tạo đồ thị
```
CREATE (a:Place {id: 'A'}),
       (b:Place {id: 'B'}),
       (c:Place {id: 'C'}),
       (d:Place {id: 'D'}),
       (e:Place {id: 'E'}),
       (f:Place {id: 'F'}),
       (g:Place {id: 'G'}),
       (d)-[:LINK {cost:4}]->(b),
       (d)-[:LINK {cost:6}]->(e),
       (b)-[:LINK {cost:1}]->(a),
       (b)-[:LINK {cost:3}]->(c),
       (a)-[:LINK {cost:2}]->(c),
       (c)-[:LINK {cost:5}]->(e),
       (f)-[:LINK {cost:1}]->(g);
```
<hr>

# Dựng đồ thị trong Graph Catalog
```
MATCH (source:Place)-[r:LINK]->(target:Place)
RETURN gds.graph.project(
  'Graph2',
  source,
  target,
  { relationshipProperties: r { .cost } },
  { undirectedRelationshipTypes: ['*'] }
)
```

# Chạy ở chế độ stream
```
MATCH (n:Place {id: 'D'})
CALL gds.spanningTree.stream('Graph2', { sourceNode: id(n), relationshipWeightProperty: 'cost' })
YIELD nodeId, parentId, weight
RETURN gds.util.asNode(nodeId).id AS node, gds.util.asNode(parentId).id AS parent, weight
ORDER BY node
```
