from easydict import EasyDict as edict 
# 字典访问，用来存储超参数 
import os
# os 模块主要用于处理文件和目录
import numpy as np
# 数据集获取
# https://ascend-professional-construction-dataset.obs.myhuaweicloud.com/deep-learning/flower_photos_train.zip
# https://ascend-professional-construction-dataset.obs.myhuaweicloud.com/deep-learning/flower_photos_test.zip
# 科学计算库
import matplotlib.pyplot as plt # 绘图库
import mindspore # MindSpore 库
import mindspore.dataset as ds # 数据集处理模块
from mindspore.dataset import vision # 图像增强模块
# from mindspore.dataset.vision import c_transforms as vision # 图像增强模块
from mindspore import context # 环境设置模块
import mindspore.nn as nn # 神经网络模块
from mindspore.train import Model # 模型编译
from mindspore.nn.optim.momentum import Momentum # 动量优化器
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig, LossMonitor # 模型保存设置
from mindspore import Tensor # 张量
from mindspore.train.serialization import export # 模型导出
from mindspore.train.loss_scale_manager import FixedLossScaleManager # 损失值平滑处理
from mindspore.train.serialization import load_checkpoint, load_param_into_net # 模型加载
import mindspore.ops as ops # 常见算子操作
# 设置 MindSpore 的执行模式和设备
mindspore.set_device('CPU')
context.set_context(mode=context.GRAPH_MODE)
# context.set_context(mode=context.GRAPH_MODE, device_target="CPU")

cfg = edict({
    'data_path': 'flower_photos_train',	#训练数据集路径
    'test_path':'flower_photos_test',	#测试数据集路径 
    'data_size': 3616,
    'HEIGHT': 224,  # 图片高度
    'WIDTH': 224, # 图片宽度 
    '_R_MEAN': 123.68, # 自定义的均值
    '_G_MEAN': 116.78,
    '_B_MEAN': 103.94,
    '_R_STD': 1, # 自定义的标准差
    '_G_STD': 1,
    '_B_STD':1,
    '_RESIZE_SIDE_MIN': 256, # 图像增强 resize 最小值
    '_RESIZE_SIDE_MAX': 512,
    'batch_size': 32, # 批次大小 
    'num_class': 5,	# 分类类别 
    'epoch_size': 5, # 训练次数 
    'loss_scale_num':1024,
    'prefix': 'resnet-ai',  # 模型保存的名称
    'directory': './model_resnet',  # 模型保存的路径
    'save_checkpoint_steps': 10, # 每隔 10 步保存 ckpt
})
# 数据处理
def read_data(path,config,usage="train"):
    # 从目录中读取图像的源数据集。
    dataset = ds.ImageFolderDataset(path, class_indexing={'daisy':0,'dandelion':1,'roses':2,'sunflowers':3,'tulips':4})
    # define map operations 
    # 图像解码算子
    decode_op = vision.Decode() 
    # 图像正则化算子
    normalize_op = vision.Normalize(mean=[cfg._R_MEAN, cfg._G_MEAN, cfg._B_MEAN], std=[cfg._R_STD, cfg._G_STD, cfg._B_STD])
    # 图像调整大小算子
    resize_op = vision.Resize(cfg._RESIZE_SIDE_MIN) 
    # 图像裁剪算子
    center_crop_op = vision.CenterCrop((cfg.HEIGHT, cfg.WIDTH)) 
    # 图像随机水平翻转算子
    horizontal_flip_op = vision.RandomHorizontalFlip() 
    # 图像通道数转换算子
    channelswap_op = vision.HWC2CHW()
    # 图像随机裁剪解码编码调整大小算子
    random_crop_decode_resize_op = vision.RandomCropDecodeResize((cfg.HEIGHT, cfg.WIDTH), (0.5, 1.0), (1.0, 1.0), max_attempts=100)
    # 只对训练集做的预处理操作
    if usage == 'train':
        dataset = dataset.map(input_columns="image", operations=random_crop_decode_resize_op) 
        dataset = dataset.map(input_columns="image", operations=horizontal_flip_op)
    # 只对测试集做的预处理操作
    else:
        dataset = dataset.map(input_columns="image", operations=decode_op) 
        dataset = dataset.map(input_columns="image", operations=resize_op) 
        dataset = dataset.map(input_columns="image", operations=center_crop_op)
    # 对全部数据集做的预处理操作
    dataset = dataset.map(input_columns="image", operations=normalize_op) 
    dataset = dataset.map(input_columns="image", operations=channelswap_op)
    # 对训练集做的批次处理
    if usage == 'train':
        dataset = dataset.shuffle(buffer_size=10000) # 10000大小缓存池用于打乱数据。
        dataset = dataset.batch(cfg.batch_size, drop_remainder=True)
    # 对测试集做的批次处理
    else:
        dataset = dataset.batch(1, drop_remainder=True)
    # 数据增强
    dataset = dataset.repeat(1) 
    dataset.map_model = 4 
    return dataset

# 查看训练集和测试集的数量
de_train = read_data(cfg.data_path,cfg,usage="train") 
de_test = read_data(cfg.test_path,cfg,usage="test")
print('训练数据集数量：',de_train.get_dataset_size()*cfg.batch_size) # get_dataset_size()获取批处理的大小。
print('测试数据集数量：',de_test.get_dataset_size())
# 查看训练集的样图
data_next = de_train.create_dict_iterator(output_numpy=True).__next__() 
print('通道数/图像长/宽：', data_next['image'][0,...].shape)
print('一张图像的标签样式：', data_next['label'][0])  # 一共 5 类，用 0-4 的数字表达类别。
# plt.figure() 
# plt.imshow(data_next['image'][0,0,...]) 
# plt.colorbar()
# plt.grid(False)
# plt.show()








