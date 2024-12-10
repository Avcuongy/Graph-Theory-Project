# Tạo đồ thị

```
CREATE
  (v1:Node {name: 'v1'}),
  (v2:Node {name: 'v2'}),
  (v3:Node {name: 'v3'}),
  (v4:Node {name: 'v4'}),
  (v5:Node {name: 'v5'}),
  (v6:Node {name: 'v6'}),
  (v7:Node {name: 'v7'}),
  (v8:Node {name: 'v8'}),
  (v9:Node {name: 'v9'}),

  // Tạo mối quan hệ vô hướng
  (v1)-[:CONNECTED {weight: 4}]->(v2),
  (v2)-[:CONNECTED {weight: 4}]->(v1),

  (v1)-[:CONNECTED {weight: 8}]->(v8),
  (v8)-[:CONNECTED {weight: 8}]->(v1),

  (v2)-[:CONNECTED {weight: 8}]->(v3),
  (v3)-[:CONNECTED {weight: 8}]->(v2),

  (v2)-[:CONNECTED {weight: 11}]->(v8),
  (v8)-[:CONNECTED {weight: 11}]->(v2),

  (v3)-[:CONNECTED {weight: 7}]->(v4),
  (v4)-[:CONNECTED {weight: 7}]->(v3),

  (v3)-[:CONNECTED {weight: 4}]->(v6),
  (v6)-[:CONNECTED {weight: 4}]->(v3),

  (v3)-[:CONNECTED {weight: 2}]->(v9),
  (v9)-[:CONNECTED {weight: 2}]->(v3),

  (v4)-[:CONNECTED {weight: 9}]->(v5),
  (v5)-[:CONNECTED {weight: 9}]->(v4),

  (v4)-[:CONNECTED {weight: 14}]->(v6),
  (v6)-[:CONNECTED {weight: 14}]->(v4),

  (v5)-[:CONNECTED {weight: 10}]->(v6),
  (v6)-[:CONNECTED {weight: 10}]->(v5),

  (v6)-[:CONNECTED {weight: 2}]->(v7),
  (v7)-[:CONNECTED {weight: 2}]->(v6),

  (v7)-[:CONNECTED {weight: 1}]->(v8),
  (v8)-[:CONNECTED {weight: 1}]->(v7),

  (v7)-[:CONNECTED {weight: 6}]->(v9),
  (v9)-[:CONNECTED {weight: 6}]->(v7),

  (v8)-[:CONNECTED {weight: 7}]->(v9),
  (v9)-[:CONNECTED {weight: 7}]->(v8)
```
