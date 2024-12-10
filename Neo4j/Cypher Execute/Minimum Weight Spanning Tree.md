# Tạo 
CALL gds.graph.project(
  'myGraph',  // Tên của đồ thị
  'Node',  // Nhãn của các nút
  'CONNECTED',  // Loại mối quan hệ
  { relationshipProperties: 'weight' }  // Các thuộc tính mối quan hệ (ở đây là 'weight')
)
