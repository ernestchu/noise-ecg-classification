import torch.nn as nn

encoding = '.NLRAaJSVF[!]ejE/fxQ|'
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(252, 500),
            nn.ReLU(),
            nn.BatchNorm1d(500),
            nn.Dropout(0.3),
            nn.Linear(500, 1000),
            nn.ReLU(),
            nn.BatchNorm1d(1000),
            nn.Dropout(0.3),
            nn.Linear(1000, 1000),
            nn.ReLU(),
            nn.BatchNorm1d(1000),
            nn.Dropout(0.3),
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.BatchNorm1d(500),
            nn.Dropout(0.3),
            nn.Linear(500, len(encoding))
        )
    def forward(self, x):
        x = self.fc(x)
        return x