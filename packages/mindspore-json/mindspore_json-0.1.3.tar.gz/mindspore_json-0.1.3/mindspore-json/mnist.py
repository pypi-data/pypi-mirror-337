#导入相关依赖库
import os
from matplotlib import pyplot as plt
import numpy as np
import mindspore as ms
import mindspore.context as context
import mindspore.dataset as ds
import mindspore.dataset.transforms.c_transforms as C
import mindspore.dataset.vision.c_transforms as CV
from mindspore.nn.metrics import Accuracy
from mindspore import nn
from mindspore.train import Model
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig, LossMonitor, TimeMonitor
context.set_context(mode=context.GRAPH_MODE, device_target='CPU')

# 数据读取
DATA_DIR_TRAIN = "MNIST/train" # 训练集信息
DATA_DIR_TEST = "MNIST/test" # 测试集信息
#读取数据
ds_train = ds.MnistDataset(DATA_DIR_TRAIN)
ds_test = ds.MnistDataset(DATA_DIR_TEST ) 
#显示数据集的相关特性
print('训练数据集数量：',ds_train.get_dataset_size())
print('测试数据集数量：',ds_test.get_dataset_size())
image=ds_train.create_dict_iterator().__next__()
print('图像长/宽/通道数：',image['image'].shape)
print('一张图像的标签样式：',image['label']) #一共 10 类，用 0-9 的数字表达类别。

# 数据处理
def create_dataset(training=True, batch_size=128, resize=(28, 28),rescale=1/255, shift=0, buffer_size=64):
 ds = ms.dataset.MnistDataset(DATA_DIR_TRAIN if training else DATA_DIR_TEST)
 # 定义 Map 操作尺寸缩放，归一化和通道变换
 resize_op = CV.Resize(resize)
 rescale_op = CV.Rescale(rescale,shift)
 hwc2chw_op = CV.HWC2CHW()
 # 对数据集进行 map 操作
 ds = ds.map(input_columns="image", operations=[rescale_op,resize_op, hwc2chw_op])
 ds = ds.map(input_columns="label", operations=C.TypeCast(ms.int32))
 #设定打乱操作参数和 batchsize 大小
 ds = ds.shuffle(buffer_size=buffer_size)
 ds = ds.batch(batch_size, drop_remainder=True)
 return ds

# 样本可视化
#显示前 10 张图片以及对应标签,检查图片是否是正确的数据集
ds = create_dataset(training=False)
data = ds.create_dict_iterator().__next__()
images = data['image'].asnumpy()
labels = data['label'].asnumpy()
plt.figure(figsize=(15,5))
for i in range(1,11):
 plt.subplot(2, 5, i)
 plt.imshow(np.squeeze(images[i]))
 plt.title('Number: %s' % labels[i])
 plt.xticks([])
plt.show()

# 定义网络
#创建模型。模型包括 3 个全连接层，最后输出层使用 softmax 进行多分类，共分成（0-9）10 类
class ForwardNN(nn.Cell): 
 def __init__(self):
  super(ForwardNN, self).__init__()
  self.flatten = nn.Flatten()
  self.fc1 = nn.Dense(784, 512, activation='relu') 
  self.fc2 = nn.Dense(512, 128, activation='relu')
  self.fc3 = nn.Dense(128, 10, activation=None)
 
 
 def construct(self, input_x):
  output = self.flatten(input_x)
  output = self.fc1(output)
  output = self.fc2(output) 
  output = self.fc3(output)
  return output

#创建网络，损失函数，评估指标 优化器，设定相关超参数
lr = 0.001
num_epoch = 10
momentum = 0.9
net = ForwardNN()
loss = nn.loss.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
metrics={"Accuracy": Accuracy()}
opt = nn.Adam(net.trainable_params(), lr)

# 开始训练
#编译模型
model = Model(net, loss, opt, metrics)
config_ck = CheckpointConfig(save_checkpoint_steps=1875, keep_checkpoint_max=10)
ckpoint_cb = ModelCheckpoint(prefix="checkpoint_net",directory = "./ckpt" ,config=config_ck)
#生成数据集
ds_eval = create_dataset(False, batch_size=32)
ds_train = create_dataset(batch_size=32)
#训练模型
loss_cb = LossMonitor(per_print_times=1875)
time_cb = TimeMonitor(data_size=ds_train.get_dataset_size())
print("============== Starting Training ==============")
model.train(num_epoch, ds_train,callbacks=[ckpoint_cb,loss_cb,time_cb ],dataset_sink_mode=False)


# 模型评估
#使用测试集评估模型，打印总体准确率
metrics=model.eval(ds_eval)
print(metrics)















































