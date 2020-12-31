import torch
import torch.nn as nn
import numpy as np
import h5py
import os
from ECG_classifier import Model

encoding = 'NAVR'
freq = [0]*len(encoding)

class NSTDB(torch.utils.data.Dataset):
    def __init__(self):
        self.h5_list = []
        for root, dirs, files in os.walk('../segmentation'):
            for f in files:
                path = os.path.join(root, f)
                with h5py.File(path, 'r') as h5:
                    if h5['MLII'][:].size != 252:
                        continue
                    freq[encoding.index(h5['label'][()])] += 1
                self.h5_list.append(os.path.join(root, f))
        
    def __getitem__(self, index):
        with h5py.File(self.h5_list[index], 'r') as f:
            index = f['index'][()]
            MLII = torch.tensor(f['MLII'][:])
            label = torch.tensor(encoding.index(f['label'][()]))
            return {
                'index': index,
                'MLII': MLII.float(),
                'label': label,
            }
    def __len__(self):
        return len(self.h5_list)
dataset = NSTDB()

index, MLII, label = dataset[10000].values()
print('Label:', label)
print('Length:', len(dataset))
print('freq:', freq)
weight = max(freq)/torch.tensor(freq)
print('Weight', weight)

dataset_train, dataset_val = torch.utils.data.random_split(dataset, [int(0.9*len(dataset)), len(dataset)-int(0.9*len(dataset))])
print(len(dataset_train), len(dataset_val))
from torch.utils.data import DataLoader
BATCH_SIZE = 512
train_loader = DataLoader(dataset_train, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(dataset_val, batch_size=BATCH_SIZE, shuffle=True)

model = Model().cuda()

criterion = nn.CrossEntropyLoss(weight=weight).cuda()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3, momentum=0.9)

def train(input_data, model, criterion, optimizer):
    model.train()
    loss_list = []
    total_count = 0
    acc_count = 0
    for data in input_data:
        index, MLII, label = data['index'], data['MLII'].cuda(), data['label'].cuda()
        
        optimizer.zero_grad()
        out = model(MLII)
        loss = criterion(out, label)
        loss.backward()
        optimizer.step()
        
        _, pred = torch.max(out, 1)
        total_count += label.shape[0]
        acc_count += (pred == label).sum().item()
        loss_list.append(loss.item())
        
    acc = acc_count/total_count
    loss = sum(loss_list)/len(loss_list)
    return acc, loss

def val(input_data, model, criterion):
    model.train()
    loss_list = []
    total_count = 0
    acc_count = 0
    with torch.no_grad():
        for data in input_data:
            index, MLII, label = data['index'], data['MLII'].cuda(), data['label'].cuda()
        
            out = model(MLII)
            loss = criterion(out, label)

            _, pred = torch.max(out, 1)
            total_count += label.shape[0]
            acc_count += (pred == label).sum().item()
            loss_list.append(loss.item())
        
    acc = acc_count/total_count
    loss = sum(loss_list)/len(loss_list)
    return acc, loss

max_epochs = 50
log_interval = 1

train_acc_list = []
train_loss_list = []
val_acc_list = []
val_loss_list = []

min_loss = 1000000
best_model = None

print("Start training...")
for epoch in range(1, max_epochs+1):
    train_acc, train_loss = train(train_loader, model, criterion, optimizer)
    val_acc, val_loss = val(val_loader, model, criterion)
    
    train_acc_list.append(train_acc)
    train_loss_list.append(train_loss)
    val_acc_list.append(val_acc)
    val_loss_list.append(val_loss)
    
    if val_loss < min_loss:
        min_loss = val_loss
        best_model = model.state_dict()
        
    if epoch % log_interval == 0:
        print('')
        print('=' * 20, 'Epoch', epoch, '=' * 20)
        print('Train Acc: {:.6f} Train Loss: {:.6f}'.format(train_acc, train_loss))
        print('  Val Acc: {:.6f}   Val Loss: {:.6f}'.format(val_acc, val_loss))
        
torch.save(best_model, 'ECG_classifier_params.pth')
        
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))
plt.plot(range(len(train_loss_list)), train_loss_list)
plt.plot(range(len(val_loss_list)), val_loss_list, c='r')
plt.legend(['train_loss', 'val'])
plt.title('Loss')
plt.savefig('Loss.png')
plt.figure(figsize=(12, 4))
plt.plot(range(len(train_acc_list)), train_acc_list)
plt.plot(range(len(val_acc_list)), val_acc_list, c='r')
plt.legend(['train', 'val'])
plt.savefig('Acc.png')