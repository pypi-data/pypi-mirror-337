import pandas as pd 
import numpy as np 
from sklearn import tree
import pydotplus

# 安装 graphviz 库，用于生成决策树图示
# https://graphviz.gitlab.io/download/

#生成决策树
def createTree(trainingData):
    data = trainingData.iloc[:, :-1]  # 特征矩阵
    labels = trainingData.iloc[:, -1]  # 标签
    trainedTree = tree.DecisionTreeClassifier(criterion="entropy")  # 分类决策树
    trainedTree.fit(data, labels)  # 训练
    return trainedTree

def showtree2pdf(trainedTree,finename):
    dot_data = tree.export_graphviz(trainedTree, out_file=None) #将树导出为 Graphviz 格式
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf(finename)  #保存树图到本地，格式为 pdf

def data2vectoc(data):
    names = data.columns[:-1] 
    for i in names:
        col = pd.Categorical(data[i]) 
        data[i] = col.codes
    return data
data = pd.read_table("tennis.txt",header=None,sep='\t') #读取训练数据 
trainingvec=data2vectoc(data) #向量化数据
decisionTree=createTree(trainingvec) #创建决策树
showtree2pdf(decisionTree,"tennis.pdf")  #图示决策树

testVec = [0,0,1,1] # 天气晴、气温冷、湿度高、风力强
print(decisionTree.predict(np.array(testVec).reshape(1,-1)))  #预测

# 天气：0-晴    1-阴    2-雨
# 气温：0-冷    1-温    2-热
# 湿度：0-正常    1-高
# 风力：0-弱    1-强