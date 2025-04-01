{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4e9f31bf-3a06-4f9a-9b54-171af093eb6c",
   "metadata": {},
   "outputs": [],
   "source": [
    "#导入相关依赖库\n",
    "import  os\n",
    "from matplotlib import pyplot as plt\n",
    "import numpy as np\n",
    "\n",
    "import mindspore as ms\n",
    "import mindspore.context as context\n",
    "import mindspore.dataset as ds\n",
    "import mindspore.dataset.transforms.c_transforms as C\n",
    "import mindspore.dataset.vision.c_transforms as CV\n",
    "from mindspore.nn.metrics import Accuracy\n",
    "\n",
    "from mindspore import nn\n",
    "from mindspore.train import Model\n",
    "from mindspore.train.callback import ModelCheckpoint, CheckpointConfig, LossMonitor, TimeMonitor\n",
    "\n",
    "context.set_context(mode=context.GRAPH_MODE, device_target='CPU')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "2d741e07-55aa-4889-94da-7be02a6f6443",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "训练数据集数量： 60000\n",
      "测试数据集数量： 10000\n",
      "图像长/宽/通道数： (28, 28, 1)\n",
      "一张图像的标签样式： 9\n"
     ]
    }
   ],
   "source": [
    "DATA_DIR_TRAIN = \"MNIST/train\" # 训练集信息\n",
    "DATA_DIR_TEST = \"MNIST/test\" # 测试集信息\n",
    "#读取数据\n",
    "ds_train = ds.MnistDataset(DATA_DIR_TRAIN)\n",
    "ds_test = ds.MnistDataset(DATA_DIR_TEST ) \n",
    "#显示数据集的相关特性\n",
    "print('训练数据集数量：',ds_train.get_dataset_size())\n",
    "print('测试数据集数量：',ds_test.get_dataset_size())\n",
    "image=ds_train.create_dict_iterator().__next__()\n",
    "print('图像长/宽/通道数：',image['image'].shape)\n",
    "print('一张图像的标签样式：',image['label'])    #一共10类，用0-9的数字表达类别。\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "3e9257c9-3129-4040-99da-308a422beccc",
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_dataset(training=True, batch_size=128, resize=(28, 28),\n",
    "                   rescale=1/255, shift=0, buffer_size=64):\n",
    "    ds = ms.dataset.MnistDataset(DATA_DIR_TRAIN if training else DATA_DIR_TEST)\n",
    "    # 定义Map操作尺寸缩放，归一化和通道变换\n",
    "    resize_op = CV.Resize(resize)\n",
    "    rescale_op = CV.Rescale(rescale,shift)\n",
    "    hwc2chw_op = CV.HWC2CHW()\n",
    "    # 对数据集进行map操作\n",
    "    ds = ds.map(input_columns=\"image\", operations=[rescale_op,resize_op, hwc2chw_op])\n",
    "    ds = ds.map(input_columns=\"label\", operations=C.TypeCast(ms.int32))\n",
    "    #设定打乱操作参数和batchsize大小\n",
    "    ds = ds.shuffle(buffer_size=buffer_size)\n",
    "    ds = ds.batch(batch_size, drop_remainder=True)\n",
    "    return ds\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "54bc435b-4e62-4051-9dd2-e1089f330b09",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:30:47.882.322 [mindspore/dataset/core/validator_helpers.py:744] 'Resize' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Resize' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:30:47.883.864 [mindspore/dataset/core/validator_helpers.py:744] 'Rescale' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Rescale' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:30:47.884.773 [mindspore/dataset/core/validator_helpers.py:744] 'HWC2CHW' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'HWC2CHW' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:30:47.885.928 [mindspore/dataset/core/validator_helpers.py:744] 'TypeCast' from mindspore.dataset.transforms.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'TypeCast' from mindspore.dataset.transforms instead.\n"
     ]
    },
    {
     "data": {
      "image/png": "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FcV/lgg/8lu2ffv26ejRo+rUqVOpbTNnztTMmTP1z3/+0/YiDniNDIcmJydHhw8fVpMmTcK2BoD8VgzvoVFVkeGyJSQkKD4+Xt9++22pbQcOHFCtWrVKfGTwTMJH8DzUtm1bjRgxQs8991zxVIqfxMbGqnHjxqW+pX/+/Pmerefll19WTk5O8fM333xTBw8eVHJysiSpe/fuatu2rZ544gnjBJxDhw5V6DxOxk/++9//1pVXXqmzzjpL7777rid/mwuEgvyWnd+77rpLS5cuLfF47rnnJP34+felS5d68vEgoKLIcNkZPnnyZIn1/OThhx+WZVkaPHhwhc4HeIH88h4a/kaGy8/wDTfcoPT0dH3wwQfFtcOHD2vZsmW69NJLFRFxZrZqaJN77De/+Y1eeeUVbd++vdSdArfddptmzZql2267TT169NC6dev09ddfe7aWhg0bqm/fvho9erQyMzM1Z84cJSUlFY+NjIiI0Isvvqjk5GR16tRJo0ePVvPmzfXtt99q9erVio2N1TvvvFPueZYuXarRo0drwYIFZX4BW05OjgYNGqSjR4/q17/+tZYvX15ie9u2bdWnT59K/cxAZZDfUbavO//883X++eeXqP30UbxOnTppyJAhof6ogGvI8Cjb12VkZOi8887T8OHD1bFjR0nS+++/rxUrVmjw4MG65pprXPm5gVCR31G2r+M9NPyADI8q87WpqalasmSJhg4dqilTpigYDOr3v/+98vPzNXPmTDd+7CqJBpTHkpKSNGLECC1atKjUtvvvv1+HDh3Sm2++qSVLlig5OVnvvfeemjZt6slapk2bpq1btyotLU05OTm67LLLNH/+fNWpU6f4Nf3799f69ev18MMP65lnntHx48cVHx+v3r176/bbb3d1PUeOHFF6erokGT8fPHLkSC6eCCvyC/gbGbZXv359XXXVVfrggw+0aNEiFRYWKikpSTNnztTdd999xv7NK/yD/NrjPTT8gAyXLS4uTh999JHuvvtuPfXUU8rPz1efPn306quvqmvXrq6fr6oIWKF8SxcAAAAAAABQQfz1FgAAAAAAADxFAwoAAAAAAACeogEFAAAAAAAAT9GAAgAAAAAAgKdoQAEAAAAAAMBTNKAAAAAAAADgqSivDjxv3jzNnj1bGRkZ6tq1q+bOnatevXqVu19RUZEOHDigmJgYBQIB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\n",
      "text/plain": [
       "<Figure size 1500x500 with 10 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#显示前10张图片以及对应标签,检查图片是否是正确的数据集\n",
    "ds = create_dataset(training=False)\n",
    "data = ds.create_dict_iterator().__next__()\n",
    "images = data['image'].asnumpy()\n",
    "labels = data['label'].asnumpy()\n",
    "plt.figure(figsize=(15,5))\n",
    "for i in range(1,11):\n",
    "    plt.subplot(2, 5, i)\n",
    "    plt.imshow(np.squeeze(images[i]))\n",
    "    plt.title('Number: %s' % labels[i])\n",
    "    plt.xticks([])\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "7a2901c5-58b8-4f6d-9faf-6cba228c8e2c",
   "metadata": {},
   "outputs": [],
   "source": [
    "#创建模型。模型包括3个全连接层，最后输出层使用softmax进行多分类，共分成（0-9）10类\n",
    "class ForwardNN(nn.Cell):      \n",
    "    def __init__(self):\n",
    "        super(ForwardNN, self).__init__()\n",
    "        self.flatten = nn.Flatten()\n",
    "        self.fc1 = nn.Dense(784, 512, activation='relu')  \n",
    "        self.fc2 = nn.Dense(512, 128, activation='relu')\n",
    "        self.fc3 = nn.Dense(128, 10, activation=None)\n",
    "       \n",
    "    \n",
    "    def construct(self, input_x):\n",
    "        output = self.flatten(input_x)\n",
    "        output = self.fc1(output)\n",
    "        output = self.fc2(output) \n",
    "        output = self.fc3(output)\n",
    "        return output  \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e4c56557-967f-4716-9684-60b53ee6c31c",
   "metadata": {},
   "outputs": [],
   "source": [
    "#创建网络，损失函数，评估指标  优化器，设定相关超参数\n",
    "lr = 0.001\n",
    "num_epoch = 10\n",
    "momentum = 0.9\n",
    "\n",
    "net = ForwardNN()\n",
    "loss = nn.loss.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')\n",
    "metrics={\"Accuracy\": Accuracy()}\n",
    "opt = nn.Adam(net.trainable_params(), lr) \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "be50a3d2-07a9-49bd-b908-ffa73f403adc",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.885.683 [mindspore/dataset/core/validator_helpers.py:744] 'Resize' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Resize' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.886.806 [mindspore/dataset/core/validator_helpers.py:744] 'Rescale' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Rescale' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.888.144 [mindspore/dataset/core/validator_helpers.py:744] 'HWC2CHW' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'HWC2CHW' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.889.817 [mindspore/dataset/core/validator_helpers.py:744] 'TypeCast' from mindspore.dataset.transforms.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'TypeCast' from mindspore.dataset.transforms instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.893.211 [mindspore/dataset/core/validator_helpers.py:744] 'Resize' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Resize' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.894.373 [mindspore/dataset/core/validator_helpers.py:744] 'Rescale' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'Rescale' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.895.440 [mindspore/dataset/core/validator_helpers.py:744] 'HWC2CHW' from mindspore.dataset.vision.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'HWC2CHW' from mindspore.dataset.vision instead.\n",
      "[WARNING] ME(41085:139958250325824,MainProcess):2024-08-14-17:31:05.896.338 [mindspore/dataset/core/validator_helpers.py:744] 'TypeCast' from mindspore.dataset.transforms.c_transforms is deprecated from version 1.8 and will be removed in a future version. Use 'TypeCast' from mindspore.dataset.transforms instead.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "============== Starting Training ==============\n",
      "epoch: 1 step: 1875, loss is 0.01147345919162035\n",
      "Train epoch time: 7148.100 ms, per step time: 3.812 ms\n",
      "epoch: 2 step: 1875, loss is 0.023888975381851196\n",
      "Train epoch time: 6309.191 ms, per step time: 3.365 ms\n",
      "epoch: 3 step: 1875, loss is 0.11368030309677124\n",
      "Train epoch time: 6457.958 ms, per step time: 3.444 ms\n",
      "epoch: 4 step: 1875, loss is 0.017362091690301895\n",
      "Train epoch time: 7455.979 ms, per step time: 3.977 ms\n",
      "epoch: 5 step: 1875, loss is 0.0007836223230697215\n",
      "Train epoch time: 6617.086 ms, per step time: 3.529 ms\n",
      "epoch: 6 step: 1875, loss is 0.01729661412537098\n",
      "Train epoch time: 6565.260 ms, per step time: 3.501 ms\n",
      "epoch: 7 step: 1875, loss is 0.001522732782177627\n",
      "Train epoch time: 6767.596 ms, per step time: 3.609 ms\n",
      "epoch: 8 step: 1875, loss is 0.004574342165142298\n",
      "Train epoch time: 6445.516 ms, per step time: 3.438 ms\n",
      "epoch: 9 step: 1875, loss is 0.0011980949202552438\n",
      "Train epoch time: 6291.481 ms, per step time: 3.355 ms\n",
      "epoch: 10 step: 1875, loss is 0.007185689173638821\n",
      "Train epoch time: 6420.575 ms, per step time: 3.424 ms\n"
     ]
    }
   ],
   "source": [
    "#编译模型\n",
    "model = Model(net, loss, opt, metrics)\n",
    "config_ck = CheckpointConfig(save_checkpoint_steps=1875, keep_checkpoint_max=10)\n",
    "ckpoint_cb = ModelCheckpoint(prefix=\"checkpoint_net\",directory = \"./ckpt\" ,config=config_ck)\n",
    "#生成数据集\n",
    "ds_eval = create_dataset(False, batch_size=32)\n",
    "ds_train = create_dataset(batch_size=32)\n",
    "#训练模型\n",
    "loss_cb = LossMonitor(per_print_times=1875)\n",
    "time_cb = TimeMonitor(data_size=ds_train.get_dataset_size())\n",
    "print(\"============== Starting Training ==============\")\n",
    "model.train(num_epoch, ds_train,callbacks=[ckpoint_cb,loss_cb,time_cb ],dataset_sink_mode=False)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "d0bbeaec-323d-4e38-9379-1123ce206ab6",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'Accuracy': 0.9797676282051282}\n"
     ]
    }
   ],
   "source": [
    "#使用测试集评估模型，打印总体准确率\n",
    "metrics=model.eval(ds_eval)\n",
    "print(metrics)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4f7ee352-6cfd-423e-bd9e-e0ba5e419bf2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "PyTorch-1.8",
   "language": "python",
   "name": "pytorch-1.8"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
