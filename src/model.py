import torch
from torch import nn
from  monai.networks.nets import ResNetFeatures


class CustomResNet(nn.Module):
    def __init__(self, model = 'resnet18', pretrained=True, spatial_dims=3, in_channels=1, num_classes=3):
        super().__init__()
        self.base_model = ResNetFeatures(model, pretrained=pretrained, spatial_dims=spatial_dims, in_channels=in_channels)
        self.avgpool = nn.AdaptiveAvgPool3d((1,1,1))
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.base_model(x)
        x = self.avgpool(x[-1])
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x