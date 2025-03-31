from PepperPepper.environment import torch, nn, profile, trunc_normal_
from PepperPepper.layers import ResidualBlock
from PepperPepper.layers import IRGradOri, IRFixOri





class up_conv(nn.Module):
    """
    Up Convolution Block
    """
    def __init__(self, in_ch, out_ch):
        super(up_conv, self).__init__()
        self.up = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.up(x)
        return x




class IRGS(nn.Module):
    def __init__(self, dim):
        super(IRGS, self).__init__()
        self.dim = dim

        self.IRfixori = IRGradOri(dim)
        self.BN = nn.BatchNorm2d(dim)
        self.conv = nn.Sequential(
            nn.Conv2d(dim * 2, dim, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(dim),
            nn.ReLU(inplace=True),
        )


    def forward(self, x):
        f = self.IRfixori(x)
        # f = v * m
        # f = self.BN(f)


        out = torch.cat((f, x), dim=1)
        out = self.conv(out)
        return out







class IRUNet(nn.Module):
    def __init__(self, in_dim = 3, dim=32, num_classes=1):
        super().__init__()
        self.title = 'IRUNet'
        self.in_dim = in_dim
        self.dim = dim
        self.num_classes = num_classes

        self.downsample = nn.MaxPool2d(2, 2)
        self.upsample = nn.Upsample(scale_factor=2)

        self.downlayer1 = ResidualBlock(in_channels=in_dim, out_channels=dim * 1)
        self.downlayer2 = ResidualBlock(in_channels=dim * 1 , out_channels=dim * 2)
        self.downlayer3 = ResidualBlock(in_channels=dim * 2, out_channels=dim * 4)
        self.downlayer4 = ResidualBlock(in_channels=dim * 4, out_channels=dim * 8)

        # self.skip1 = IRGradSkip(dim=dim * 1, kernel_size=[5])
        # self.skip2 = IRGradSkip(dim=dim * 2, kernel_size=[5])
        # self.skip3 = IRGradSkip(dim=dim * 4, kernel_size=[5])


        self.skip1 = IRGS(dim = dim * 1 )
        self.skip2 = IRGS(dim = dim * 2 )
        self.skip3 = IRGS(dim = dim * 4 )



        self.up_conv3 = up_conv(dim * 8, dim * 4)
        self.up_conv2 = up_conv(dim * 4, dim * 2)
        self.up_conv1 = up_conv(dim * 2, dim * 1)
        self.uplayer3 = ResidualBlock(in_channels=dim * 8, out_channels=dim * 4)
        self.uplayer2 = ResidualBlock(in_channels=dim * 4, out_channels=dim * 2)
        self.uplayer1 = ResidualBlock(in_channels=dim * 2, out_channels=dim * 1)
        self.cout = nn.Conv2d(dim, num_classes, 1)
        self.apply(self._init_weights)





    def forward(self, x):

        if x.size(1) == 1:
            x = x.repeat(1, self.in_dim, 1, 1)

        f1 = self.downlayer1(x)
        f2 = self.downlayer2(self.downsample(f1))
        f3 = self.downlayer3(self.downsample(f2))
        f4 = self.downlayer4(self.downsample(f3))


        f1 = self.skip1(f1)
        f2 = self.skip2(f2)
        f3 = self.skip3(f3)

        # print(f'f1 shape: {f1.shape}')
        # print(f'f2 shape: {f2.shape}')
        # print(f'f3 shape: {f3.shape}')
        # print(f'f4 shape: {f4.shape}')

        # print(self.upsample(f4).shape)

        d3 = self.up_conv3(f4)
        d3 = torch.cat((d3, f3), dim=1)
        d3 = self.uplayer3(d3)

        # print(f'd3 shape: {d3.shape}')




        d2 = self.up_conv2(d3)
        d2 = torch.cat((d2, f2), dim=1)
        d2 = self.uplayer2(d2)
        # print(f'd2 shape: {d2.shape}')



        d1 = self.up_conv1(d2)
        d1 = torch.cat((d1, f1), dim=1)
        d1 = self.uplayer1(d1)
        # print(f'd1 shape: {d1.shape}')


        out = self.cout(d1)







        if torch.isnan(out).any():
            print(f"[{self.__class__.__name__}] out")


        return out

    def _init_weights(self, m):
        """ 增强版权重初始化方法，支持主流网络层类型
        核心策略：
        - Transformer风格线性层初始化
        - CNN优化卷积层初始化
        - 自适应归一化层处理
        """

        # 线性层初始化（适配Transformer结构）
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=0.02)  # 截断正态分布，限制极端值
            if m.bias is not None:  # 偏置项零初始化
                nn.init.zeros_(m.bias)

                # 卷积层初始化（适配CNN结构）
        elif isinstance(m, nn.Conv2d):
            # 计算Kaiming初始化标准差
            fan_in = m.kernel_size[0] * m.kernel_size[1] * m.in_channels
            # 使用ReLU激活的推荐模式（兼容GELU/SiLU）
            nn.init.kaiming_normal_(m.weight,
                                    mode='fan_in',
                                    nonlinearity='relu')
            if m.bias is not None:  # 偏置项零初始化
                nn.init.zeros_(m.bias)

                # 归一化层初始化
        elif isinstance(m, (nn.LayerNorm, nn.BatchNorm2d)):
            nn.init.ones_(m.weight)  # 缩放系数初始为1
            nn.init.zeros_(m.bias)  # 平移系数初始为0





if __name__ == '__main__':
    model = IRUNet().cuda()
    inputs = torch.rand(1, 1, 256, 256).cuda()
    output = model(inputs)
    print(output.shape)
    flops, params = profile(model, (inputs,))

    print("-" * 50)
    print('FLOPs = ' + str(flops / 1000 ** 3) + ' G')
    print('Params = ' + str(params / 1000 ** 2) + ' M')