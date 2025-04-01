# 从 sklearn.preprocessing 里导入 StandardScaler。 
from sklearn.preprocessing import StandardScaler
# 从 sklearn.linear_model 里导入 LogisticRegression
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


# X：每一项表示租金和面积
# y：表示是否租赁该房间（0：不租，1：租） 
X=[[2200,15],[2750,20],[5000,40],[4000,20],[3300,20],[2000,10],[2500,12],[12000,80],
[2880,10],[2300,15],[1500,10],[3000,8],[2000,14],[2000,10],[2150,8],[3400,20],
[5000,20],[4000,10],[3300,15],[2000,12],[2500,14],[10000,100],[3150,10],
[2950,15],[1500,5],[3000,18],[8000,12],[2220,14],[6000,100],[3050,10]
]

y=[1,1,0,0,1,1,1,1,0,1,1,0,1,1,0,1,0,0,0,1,1,1,0,1,0,1,0,1,1,0]

ss = StandardScaler()
X_train = ss.fit_transform(X)
# print(X_train)
#调用 Lr 中的 fit 模块训练模型参数
lr = LogisticRegression()
lr.fit(X_train, y)

testX = [[2000,8]]
X_test = ss.transform(testX) 
print("待预测的值：",X_test) 
label = lr.predict(X_test) 
print("predicted label = ", label) #输出预测概率
prob = lr.predict_proba(X_test)
print("probability = ",prob)


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 可视化数据集
plt.figure(figsize=(10, 6))
plt.scatter([x[0] for x, label in zip(X, y) if label == 0], 
           [x[1] for x, label in zip(X, y) if label == 0], 
           c='red', label='不租', alpha=0.6)
plt.scatter([x[0] for x, label in zip(X, y) if label == 1], 
           [x[1] for x, label in zip(X, y) if label == 1], 
           c='blue', label='租', alpha=0.6)
plt.xlabel('租金')
plt.ylabel('面积')
plt.title('房屋租赁数据分布')
plt.legend()
plt.show()
