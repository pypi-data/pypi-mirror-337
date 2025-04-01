from sklearn.datasets import make_blobs 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X, y = make_blobs(n_samples=500,n_features=2,centers=4,random_state=1)

# print("X 的维度为：{}".format(X.shape))
# print("y 的维度为：{}".format(y.shape))

# fig, ax1 = plt.subplots(1) 
# ax1.scatter(X[:, 0], X[:, 1]
#     ,marker='o'  # 设置点的形状为圆形
#     ,s=8  # 设置点的大小
# )
# plt.show()

# color = ["red","pink","orange","green"] 
# fig, ax1 = plt.subplots(1)
# for i in range(4):
#     ax1.scatter(X[y==i, 0], X[y==i, 1]  # 根据每个点的标签绘制
#         ,marker='o'  # 设置点的形状为圆形
#         ,s=8  # 设置点的大小
#         ,c=color[i]
#     )
# plt.show()

# n_clusters = 3
# cluster1 = KMeans(n_clusters=n_clusters,random_state=3).fit(X)
# y_pred1 = cluster1.labels_
# print(y_pred1)
# centroid1 = cluster1.cluster_centers_
# print(centroid1)
# color = ["red","pink","orange","gray"] 
# fig, ax1 = plt.subplots(1)
# for i in range(n_clusters): 
#     ax1.scatter(X[y_pred1==i, 0], X[y_pred1==i, 1]
#         ,marker='o' #点的形状
#         ,s=8 #点的大小
#         ,c=color[i]
#     )

# ax1.scatter(centroid1[:,0],centroid1[:,1]
#     ,marker="x"
#     ,s=15
#     ,c="black")
# plt.show()

n_clusters = 4
cluster2 = KMeans(n_clusters=n_clusters,random_state=0).fit(X) 
y_pred2 = cluster2.labels_
centroid2 = cluster2.cluster_centers_
color = ["red","pink","orange","green"] 
fig, ax1 = plt.subplots(1)
for i in range(n_clusters): 
    ax1.scatter(X[y_pred2==i, 0], X[y_pred2==i, 1]
        ,marker='o' #点的形状
        ,s=8 #点的大小
        ,c=color[i]
    )
ax1.scatter(centroid2[:,0],centroid2[:,1]
    ,marker="x"
    ,s=15
    ,c="black")
plt.show()









