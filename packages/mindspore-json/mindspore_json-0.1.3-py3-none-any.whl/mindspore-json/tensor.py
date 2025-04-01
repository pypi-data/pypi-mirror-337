# 数组创建 Tensor
import mindspore
# cell 同时输出多行
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import numpy as np
from mindspore import Tensor
from mindspore import dtype
# 用数组创建张量
x = Tensor(np.array([[1, 2], [3, 4]]), dtype.int32)


# 用数值创建 Tensor
y = Tensor(1.0, dtype.int32)
z = Tensor(2, dtype.int32)



# 用 Bool 创建 Tensor
m = Tensor(True, dtype.bool_)


# 用 tuple 创建 Tensor
n = Tensor((1, 2, 3), dtype.int16)


# 用 list 创建 Tensor
p = Tensor([4.0, 5.0, 6.0], dtype.float64)


# 张量的属性包括形状（shape）和数据类型（dtype）。
x = Tensor(np.array([[1, 2], [3, 4]]), dtype.int32)
x.shape # 形状
x.dtype # 数据类型
x.ndim # 维度
x.size # 大小


# asnumpy()：将 Tensor 转换为 NumPy 的 array。
y = Tensor(np.array([[True, True], [False, False]]), dtype.bool_)
# 将 Tensor 数据类型转换成 NumPy
y_array = y.asnumpy()


# Tensor索引和切片
tensor = Tensor(np.array([[0, 1], [2, 3]]).astype(np.float32))
print("First row: {}".format(tensor[0]))
print("First column: {}".format(tensor[:, 0]))
print("Last column: {}".format(tensor[..., -1]))

# Tensor 拼接
data1 = Tensor(np.array([[0, 1], [2, 3]]).astype(np.float32))
data2 = Tensor(np.array([[4, 5], [6, 7]]).astype(np.float32))
op = ops.Stack()
output = op([data1, data2])
print(output)

# 数据集加载
import os
import mindspore.dataset as ds
import matplotlib.pyplot as plt
dataset_dir = "./MNIST/train" # 数据集路径
# 从 mnist dataset 读取 3 张图片
mnist_dataset = ds.MnistDataset(dataset_dir=dataset_dir, num_samples=3)
# 查看图像，设置图像大小
plt.figure(figsize=(8,8))
i = 1
# 打印 3 张子图
for dic in mnist_dataset.create_dict_iterator(output_numpy=True):
 plt.subplot(3,3,i)
 plt.imshow(dic['image'][:,:,0])
 plt.axis('off')
 i +=1
plt.show()

# 自定义数据集
import numpy as np
np.random.seed(58)
class DatasetGenerator:
#实例化数据集对象时，__init__函数被调用，用户可以在此进行数据初始化等操作。
  def __init__(self):
    self.data = np.random.sample((5, 2))
    self.label = np.random.sample((5, 1))
    #定义数据集类的__getitem__函数，使其支持随机访问，能够根据给定的索引值 index，获取数据集中的数据并返回。
    def __getitem__(self, index):
      return self.data[index], self.label[index]
    #定义数据集类的__len__函数，返回数据集的样本数量。
    def __len__(self):
      return len(self.data)
    #定义数据集类之后，就可以通过 GeneratorDataset 接口按照用户定义的方式加载并访问数据集样本。
    dataset_generator = DatasetGenerator()
    dataset = ds.GeneratorDataset(dataset_generator, ["data", "label"], shuffle=False)
    #通过 create_dict_iterator 方法获取数据
    for data in dataset.create_dict_iterator():
      print('{}'.format(data["data"]), '{}'.format(data["label"]))

# 数据增强 如：打乱、设置 batch 等。
ds.config.set_seed(58)
# 随机打乱数据顺序，buffer_size 表示数据集中进行 shuffle 操作的缓存区的大小。
dataset = dataset.shuffle(buffer_size=10)
# 对数据集进行分批，batch_size 表示每组包含的数据个数，现设置每组包含 2 个数据。
dataset = dataset.batch(batch_size=2)
for data in dataset.create_dict_iterator():
  print("data: {}".format(data["data"]))
  print("label: {}".format(data["label"]))

# 网络构建 全连接层
import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor
import numpy as np
# 构造输入张量
input_a = Tensor(np.array([[1, 1, 1], [2, 2, 2]]), ms.float32)
print(input_a)
# 构造全连接网络，输入通道为 3，输出通道为 3
net = nn.Dense(in_channels=3, out_channels=3, weight_init=1)
output = net(input_a)
print(output)

# 网络构建 卷积层
conv2d = nn.Conv2d(1, 6, 5, has_bias=False, weight_init='normal', pad_mode='valid')
input_x = Tensor(np.ones([1, 1, 32, 32]), ms.float32)
print(conv2d(input_x).shape)

# 网络构建 ReLU 层
relu = nn.ReLU()
input_x = Tensor(np.array([-1, 2, -3, 2, -1]), ms.float16)
output = relu(input_x)
print(output)

# 网络构建 池化层
max_pool2d = nn.MaxPool2d(kernel_size=2, stride=2)
input_x = Tensor(np.ones([1, 6, 28, 28]), ms.float32)
print(max_pool2d(input_x).shape)

# 网络构建 Flatten 层
flatten = nn.Flatten()
input_x = Tensor(np.ones([1, 16, 5, 5]), ms.float32)
output = flatten(input_x)
print(output.shape)

# 模型训练 损失函数
# 损失函数用来评价模型的预测值和真实值不一样的程度，在这里，使用绝对误差损失函数
# L1Loss。mindspore.nn.loss 也提供了许多其他常用的损失函数，如
# SoftmaxCrossEntropyWithLogits、MSELoss、SmoothL1Loss 等。
import numpy as np
import mindspore.nn as nn
from mindspore import Tensor
import mindspore.dataset as ds
import mindspore as ms
loss = nn.L1Loss()
output_data = Tensor(np.array([[1, 2, 3], [2, 3, 4]]).astype(np.float32))
target_data = Tensor(np.array([[0, 2, 5], [3, 1, 1]]).astype(np.float32))
print(loss(output_data, target_data))

# 优化器 深度学习优化算法大概常用的有 SGD、Adam、Ftrl、lazyadam、Momentum、RMSprop、Lars、 Proximal_ada_grad 和 lamb 这几种。






































































































































