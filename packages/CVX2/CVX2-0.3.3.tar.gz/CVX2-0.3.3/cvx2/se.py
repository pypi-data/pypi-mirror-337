import torch
from torch import nn
# from torchstat import stat  # 查看网络参数
 
# 定义SE注意力机制的类
class SE(nn.Module):
    def __init__(self, channel, ratio=16):
        super(SE, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // ratio, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // ratio, channel, bias=False),
            nn.Sigmoid()
        )
 
    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y
 
 
if __name__ == '__main__':
    # 构造输入层
    inputs = torch.rand(2,320,32,32)
    # 获取输入通道数
    channel = inputs.shape[1]
    # 模型实例化
    model = SE(channel, ratio=16)
 
    # 前向传播查看输出结果
    outputs = model(inputs)
    print(outputs.shape)  #[2, 320, 32, 32]
 
    # print(model)  # 查看模型结构
    # stat(model, input_size=[320,32,32])  # 查看参数，不需要指定batch维度