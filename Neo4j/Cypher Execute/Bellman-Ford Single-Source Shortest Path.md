# Tạo đồ thị
```
CREATE (a:Node {name: 'A'}),
       (b:Node {name: 'B'}),
       (c:Node {name: 'C'}),
       (d:Node {name: 'D'}),
       (e:Node {name: 'E'}),
       (f:Node {name: 'F'}),
       (g:Node {name: 'G'}),
       (h:Node {name: 'H'}),
       (i:Node {name: 'I'}),
       (a)-[:REL {cost: 50}]->(b),
       (a)-[:REL {cost: -50}]->(c),
       (a)-[:REL {cost: 100}]->(d),
       (b)-[:REL {cost: 40}]->(d),
       (c)-[:REL {cost: 40}]->(d),
       (c)-[:REL {cost: 80}]->(e),
       (d)-[:REL {cost: 30}]->(e),
       (d)-[:REL {cost: 80}]->(f),
       (e)-[:REL {cost: 40}]->(f),
       (g)-[:REL {cost: 40}]->(h),
       (h)-[:REL {cost: -60}]->(i),
       (i)-[:REL {cost: 10}]->(g)
```
<hr>

# Dựng đồ thị trong Graph Catalog
```
MATCH (source:Node)-[r:REL]->(target:Node)
RETURN gds.graph.project(
  'Graph3',   
  source,       
  target,      
  { relationshipProperties: r { .cost } }
)

```

# Chạy ở chế độ stream
```
MATCH (source:Node {name: 'A'})  // Lấy node nguồn (A)
CALL gds.bellmanFord.stream('myGraph', {
    sourceNode: source,         
    relationshipWeightProperty: 'cost'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, route, isNegativeCycle
RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNode,
    gds.util.asNode(targetNode).name AS targetNode,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(route) AS route,
    isNegativeCycle
ORDER BY index
```
