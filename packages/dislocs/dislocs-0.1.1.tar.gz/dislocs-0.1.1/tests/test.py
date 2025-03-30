import gmsh
import sys
import meshio
import numpy as np
import pyvista as pv
import dislocs as dl
import _okada92


# 初始化 gmsh
# gmsh.initialize(sys.argv)
# gmsh.model.add("rectangle")

# # 定义矩形的四个角点
# p1 = gmsh.model.geo.addPoint(439.60017008978974, 3924.5362397775775, -5, meshSize=10)  # 设置不同网格尺寸
# p2 = gmsh.model.geo.addPoint(429.7520925596677, 3926.272721554247, -5, meshSize=10)
# p3 = gmsh.model.geo.addPoint(430.34600430580656, 3929.6409624425814, -14.396926207859083, meshSize=10)
# p4 = gmsh.model.geo.addPoint(440.1940818359286, 3927.904480665912, -14.396926207859083, meshSize=10)


# # 定义矩形的边
# l1 = gmsh.model.geo.addLine(p1, p2)
# l2 = gmsh.model.geo.addLine(p2, p3)
# l3 = gmsh.model.geo.addLine(p3, p4)
# l4 = gmsh.model.geo.addLine(p4, p1)

# # 创建一个面
# l_lines = [l1, l2, l3, l4]
# loop = gmsh.model.geo.addCurveLoop(l_lines)
# surface = gmsh.model.geo.addPlaneSurface([loop])

# # 同步并生成网格（不使用 Transfinite 设置）
# gmsh.model.geo.synchronize()
# gmsh.model.mesh.generate(2)

# # 保存网格文件
# gmsh.write("rectangle_non_uniform.msh")

# # 关闭 gmsh
# gmsh.finalize()

# ============ 读取网格文件并可视化 ============
mesh = meshio.read("rectangle_non_uniform.msh")

# 获取三角形单元
triangles = np.array(mesh.cells_dict["triangle"])
points = np.array(mesh.points)

print(f"triangles: {triangles}")
print(f"points: {points}")

# # 可视化
# plotter = pv.Plotter()
# mesh_pv = pv.PolyData(points, np.hstack([np.full((triangles.shape[0], 1), 3), triangles]))
# plotter.add_mesh(mesh_pv, show_edges=True, color="lightblue")

# # 设置视图和坐标轴
# plotter.view_isometric()
# plotter.show_axes()
# plotter.show()

#---------------------------------------------------------------------------------------------------- 
mu = 3.3e10
nu = 0.25
obs = np.array([
    [450, 3916, 0],
    [456, 4000, -1],
    [434.6761313247287, 3935.404480665912, -5]
    ])

uc = np.array([434.6761313247287, 3925.404480665912, -5])
model = np.array([[uc[0], uc[1], uc[2],   10, 10,   280, 70,    5, 5, 5]])
print(f"model: {model}")

[U, S, E, flags] = dl.rde(obs, model, mu, nu)



# 遍历所有三角形，获取顶点坐标
triangle_vertices = np.array([points[triangle].flatten() for triangle in triangles])  # 形状 (n, 9)

ss = np.full((len(triangles), 1), 5)      # (n, 1)
ds = np.full((len(triangles), 1), 5)      # (n, 1)
ts = np.full((len(triangles), 1), 5)      # (n, 1)
triangle_data = np.hstack([triangle_vertices, ss, ds, ts])
triangle_data2 = np.hstack([triangle_vertices, ss, ds, ts])


# 打印前几个三角形的数据
print("每个三角形的顶点坐标 (x1, y1, z1, x2, y2, z2, x3, y3, z3) :")
print(triangle_vertices[:5])  # 只打印前 5 行，避免输出过长

[U2, S2, E2 ] = dl.tde(obs, triangle_data, mu, nu)
[U3, S3, E3 ] = dl.tde_meade(obs, triangle_data2, mu, nu)

#-------------------------------------------------------
# cc = np.array([447.3987425976274, 3931.9897116567467, -25.606601717798213])
# [U4, E4, S4 ] = _okada92.okada92(obs[0, :], obs[1, :], obs[2, :],  np.array(cc[0]), np.array(cc[1]), np.array(-cc[2]), np.array(10), np.array(10), np.array(45), np.array(50),np.array(0), np.array(5), np.array(0), mu, nu, np.array([0,0,0]),)

#-------------------------------------------------------
#3 [U2, S2, E2 ] = dl.tde(obs, model2, mu, nu)
#3 [U3, S3, E3 ] = dl.tde_meade(obs, model2, mu, nu)
U   = np.round(U, 12)
U2  = np.round(U2, 12)
U3  = np.round(U3, 12)
print(f"U = \n{U}")
print(f"U2 = \n{U2}")
print(f"U3 = \n{U3}")

S   = np.round(S, 12)
S2  = np.round(S2, 12)
S3  = np.round(S3, 12)
print(f"S = \n{S}")
print(f"S2 = \n{S2}")
print(f"S3 = \n{S3}")
#---------------------------------------------------------------------------------------------------- 
#---------------------------------------------------------------------------------------------------- 
#---------------------------------------------------------------------------------------------------- 
#---------------------------------------------------------------------------------------------------- 

#9 mu = 3.3e10
#9 nu = 0.25
#9 
#9 # ----------------------------------------------------------------------------------------------------
#9 # # ---------------  X axis ----------------
#9 # model = np.array([
#9 # [0, 0, -1, 4, 4,  90, 90,        5, 5, 5]  # -------- X axis
#9 # ])
#9 
#9 # obs = np.array([
#9 #     [1, -1, 0],
#9 #     [1,  1, 0],
#9 # ])
#9 # model_tde = np.array([ [-2,  0, -1,    2,  0, -1,     2,  0, -5,    5, 5, 5],
#9 #                        [-2,  0, -1,   -2,  0, -5,     2,  0, -5,    5, 5, 5],
#9 # ])
#9 # ----------- to be test!
#9 
#9 # # 1) test above adjust the order of vertes
#9 # # 2) test different ss, ds, ts, respectively
#9 
#9 # model_tde = np.array([ [-2,  0, -1,    2,  0, -1,     2,  0, -5,    5, 5, 5],
#9 #                        [-2,  0, -1,    2,  0, -5,    -2,  0, -5,    5, 5, 5],
#9 # ])
#9 # ----------------------------------------------------------------------------------------------------
#9 
#9 # # ---------------  Y axis ----------------
#9 # model = np.array([
#9 #   [0, 0, -1, 4, 4,   0, 90,        5, 5, 5] 
#9 # ])
#9 
#9 # obs = np.array([
#9 #     [-1,  1, 0],
#9 #     [ 1,  1, 0],
#9 # ])
#9 
#9 
#9 # model_tde = np.array([ [0, -2, -1,    0,  2, -1,    0,   2, -5,    5, 5, 5],
#9 #                        [0, -2, -1,    0,  -2, -5,    0,  2, -5,    5, 5, 5],
#9 # ])
#9 
#9 # model_tde = np.array([ [0, -2, -1,    0,  2, -1,    0,   2, -5,    5, 5, 5],
#9 #                        [0, -2, -1,    0,  -2, -5,   0,  2, -5,     5, 5, 5],
#9 # ])
#9 
#9 # model_tde = np.array([ [0, -2, -1,    0,   2, -5,   0,  2, -1,     5, 5, 5],
#9 #                        [0, -2, -1,    0,  2, -5,    0,  -2, -5,    5, 5, 5],
#9 # ])
#9 # ----------------------------------------------------------------------------------------------------
#9 # ---------------  vertical fault but ohter dierections ----------------
#9 model = np.array([
#9   [0, 0, 0, 2.8284, 2.8284,   45, 90,        0, 5, 0] 
#9 ])
#9 
#9 obs = np.array([
#9     [-1,  1, 0],
#9     [ 1, -1, 0],
#9     [ 0.5, 0.5, -0.5],
#9 ])
#9 
#9 
#9 # model_tde = np.array([ [-1, -1, 0,  1,  1,  0,        1,  1, -2.8284,    5, 5, 5],
#9 #                        [-1, -1, 0,  1, 1, -2.8284,   -1, -1, -2.8284,    5, 5, 5],
#9 # ])
#9 
#9 model_tde = np.array([ [-1, -1, 0,  1,  1,  0,        1,  1, -2.8284,    0, 5, 0],
#9                        [-1, -1, 0,  -1, -1, -2.8284,  1, 1, -2.8284,     0, 5, 0],
#9 ])
#9 # ----------------------------------------------------------------------------------------------------
#9 # # # ---------------  horizontal fault ----------------
#9 # model = np.array([
#9 #   # [0, 0, -1, 2., 2.,   90, 0,        10, 0, 0] 
#9 #   [0, 1, -1, 2., 2.,   90, 0,        5, 5, 5] 
#9 # ])
#9 
#9 # obs = np.array([
#9 #     [ 0.1,  0.1,  -0.9],
#9 #     [ 0.1,  0.1,  -1.1],
#9 #     [ 0.5,  0.5,  -1.0],
#9 #     # [ 0.5,  0.5,  -0.9],
#9 #     # [ 0.5,  0.5,  -1.1],
#9 # ])
#9 
#9 # # model_tde = np.array([ [  1,  -1, -1,   -1,  1, -1,   1,  1,  -1,   5, 5, 5],
#9 # #                        [ -1,  -1, -1,   -1,  1, -1,   1, -1,  -1,   5, 5, 5],
#9 # # ])
#9 
#9 # model_tde = np.array([ [  1,  -1, -1,   1,  1,  -1,   -1,  1, -1,   5, 5, 5],
#9 #                        [ -1,  -1, -1,   1, -1,  -1,   -1,  1, -1,   5, 5, 5],
#9 # ])
#9 # ----------------------------------------------------------------------------------------------------
#9 # # ---------------  Others ----------------
#9 
#9 # model = np.array([
#9 # [0, 0, -1, 4, 4,  90, 90,        5, 5, 5]  # 
#9 # ])
#9 
#9 # obs = np.array([
#9 #     # [1, -1, 0],
#9 #     # [1,  1, 0],
#9 #     [-1/3, -1/3, -3],
#9 #     [-1/3, -1/3, -14/3],
#9 #     [-1/3, -1/3, -6],
#9 #     [7,     -1,  -5],
#9 #     [-7,   -1,   -5],
#9 # ])
#9 # model_tde = np.array([ [-1, -1, -5,    1, -1, -5,    -1,  1, -4,    1, -1, 2],
#9 #                        [-1, -1, -5,   -1,  1,  0,     1, -1, -5,    1, -1, 2],
#9 # ])
#9 
#9 # # model_tde = np.array([ [-1, -1, -5,    1, -1, -5,    -1,  1, -4,    5, 5, 5],
#9 # #                        [-1, -1, -5,    1, -1, -5,    -1,  1,  0,    5, 5, 5],
#9 # # ])
#9 
#9 # ----------------------------------------------------------------------------------------------------
#9 
#9 # ----------------------------------------------------------------------------------------------------
#9 # length, width, depth, dip, strike, easting, northing, str-slip, dip-selip. opening
#9 [U, S, E, flags] = dl.rde(obs, model, mu, nu)
#9 [Utede, Stede, Etede] = dl.tde(obs, model_tde, mu, nu)
#9 [Utede2, Stede2, Etede2] = dl.tde_meade(obs, model_tde, mu, nu)
#9 
#9 print("------------------- Result OKADA, mehdi, meade ------------------------------")
#9 print(f"OKADA flags =\n {flags}")
#9 print(f"OKADA U =\n {U}")
#9 print(f"mehdi Utede =\n {Utede}")
#9 print(f"meade Utede2 =\n {Utede2}")
#9 
#9 print("-------------------  stress  ------------------------------")
#9 print(f"Okada S =\n {S}")
#9 print(f"mehdi Stede =\n {Stede}")
#9 print(f"meade Stede2 =\n {Stede2}")
#9 
#9 # print(f"E =\n {E}")
#9 # print(f"Etede =\n {Etede}")
#9 # print(f"Etede2 =\n {Etede2}")
