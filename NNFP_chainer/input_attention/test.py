import math
import argparse
import numpy as np
import numpy.random as npr
#import cupy as np #GPUを使うためのnumpy
import chainer 
from chainer import cuda, Function, Variable, optimizers
from chainer import Link, Chain
import chainer.functions as F
import chainer.links as L
import time

class Main(Chain):
	def __init__(self):
		super(Main, self).__init__(
			L1 = L.Linear(None,10),
			L2 = L.Linear(10,8),
			H1 = L.Linear(None,8),
		)
	
	def __call__(self, x):
		h1 = self.L1(x)
		z = np.array([[1,1,1,1,1,1,1,1]], dtype=np.float32)
		for i in range(5):
			print(type(z))
			z = self.H1(z)
		y = self.L2(h1)
		return y
	

def main():
	x = Variable(np.array([[0,1,0,0,1,0,1,0]], dtype=np.float32))
	y = Variable(np.array([[0,0.2,0,0,0.1,0,0.7,0]], dtype=np.float32))

	
	model = Main()
	optimizer = optimizers.Adam()
	optimizer.setup(model)

	for epoch in range(1000):
		model.zerograds()
		pred = model(x)
		loss = F.mean_squared_error(pred,y)
		loss.backward()
		optimizer.update()
	print(pred)

if __name__ == '__main__':
	main()
