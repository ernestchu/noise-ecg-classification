import torch.nn as nn

encoding = 'NAVR'
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        def convBlock(in_filters, out_filters, normalization=True):
            layers = [nn.Conv1d(in_filters, out_filters, 4, stride=2, padding=1)]
            if normalization:
                layers.append(nn.BatchNorm1d(out_filters))
            layers.append(nn.Tanh())
            return layers
        self.conv = nn.Sequential(
            *convBlock(1, 64, normalization=False),
            *convBlock(64, 128),
            *convBlock(128, 256),
            *convBlock(256, 512),
            nn.ConstantPad1d((0, 1), 0),
            nn.Conv1d(512, len(encoding), 4, padding=1, bias=False),
            nn.AdaptiveAvgPool1d(1)
        )
    def forward(self, x):
        x = self.conv(x)
        return x.reshape(x.shape[0], x.shape[1])