## Thư viện Python
import math
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


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


##------------------------------------------------------------------------------


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


##------------------------------------------------------------------------------


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


##------------------------------------------------------------------------------


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
