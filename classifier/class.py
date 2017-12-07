from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import numpy as np
import pylab as p

batch_size = 64
test_batch_size = 1000
epochs = 10
lr = 0.01
momentum = 0.5
cuda = torch.cuda.is_available()

kwargs = {'num_workers': 1, 'pin_memory': True} if cuda else {}
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=batch_size, shuffle=True, **kwargs)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=test_batch_size, shuffle=True, **kwargs)

images = torch.utils.data.DataLoader(
	datasets.MNIST('../data', train=False), batch_size = test_batch_size, shuffle= False, **kwargs)

class Net(nn.Module):
	def __init__(self):
		super(Net, self).__init__();
		self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
		self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
		self.conv2_drop = nn.Dropout2d()
		self.fc1 = nn.Linear(320, 50)
		self.fc2 = nn.Linear(50, 10)

	def forward(self, x):
		x = F.relu(F.max_pool2d(self.conv1(x), 2))
		x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
		x = x.view(-1, 320)
		x = F.relu(self.fc1(x))
		x = F.dropout(x, training=self.training)
		x = self.fc2(x)
		return F.log_softmax(x)

model = Net()
if cuda:
	mode1.cuda()
		
optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum)

def train():
	x = []
	y = []
	i = 0
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('Accuracy Vs. Generations')
	ax.set_xlabel('Generations')
	ax.set_ylabel('Accuracy (%)')
	correct = 0
	model.train()
	for batch_idx, (data, target) in enumerate(train_loader):
		i += 1
		if cuda:
			data, target = data.cuda(), target.cuda()
		data, target = Variable(data), Variable(target)
		optimizer.zero_grad()
		output = model(data)
		pred = output.data.max(1, keepdim=True)[1]
		correct += pred.eq(target.data.view_as(pred)).cpu().sum()
		x.append(i)
		y.append(100.*correct/len(train_loader.dataset))
		loss = F.nll_loss(output, target)
		loss.backward()
		optimizer.step()
	plt.plot(x, y)
	plt.show()

def test():
	model.eval();
	test_loss = 0
	correct = 0

	for data, target in test_loader:
		i += 1
		if cuda:
			data, target = data.cuda(), target.cuda()
		data, target = Variable(data, volatile=True), Variable(target)
		output = model(data)
		test_loss += F.nll_loss(output, target, size_average=False).data[0]
		pred = output.data.max(1, keepdim=True)[1]
		correct += pred.eq(target.data.view_as(pred)).cpu().sum()

		test_loss/= len(test_loader.dataset)
		print('\nTest set: Average loss: {:.4f}, Accuracy {}/{} ({:.0f}%\n'.format(test_loss, correct, len(test_loader.dataset), 100.*correct/len(test_loader.dataset)))


train()
test()