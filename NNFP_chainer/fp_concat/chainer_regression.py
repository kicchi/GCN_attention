#coding: utf-8
import math
import argparse
import copy
import numpy as np
import numpy.random as npr
#import cupy as np #GPUを使うためのnumpy
import chainer 
from chainer import cuda, Function, Variable, optimizers
from chainer import Link, Chain
import chainer.functions as F
import chainer.links as L
import time

from NNFP import load_data 
from NNFP import result_plot 
from NNFP import normalize_array
from NNFP import Deep_neural_network
from NNFP import Finger_print


delaney_params = {'target_name' : 'measured log solubility in mols per litre',
			 	 'data_file'  : 'delaney.csv',
			 	 'train' : 700,
			 	 'val' : 200,
			 	 'test' : 100}

cep_params = {'target_name' : 'PCE',
				'data_file'  : 'cep.csv',
			 	 #'train' : 20000,
			 	 'train' : 1000,
			 	 'val' : 250,
			 	 #'test' : 5000}
			 	 'test' : 100}
malaria_params = {'target_name' : 'activity',
				'data_file'  : 'malaria.csv',
			 	 'train' : 1000,
			 	 'val' : 197,
			 	 'test' : 100}

model_params = dict(fp_length = 50,      
					fp_depth = 4,       #NNの層と、FPの半径は同じ
					conv_width = 20,    #必要なパラメータはこれだけ（？）
					h1_size = 100,      #最上位の中間層のサイズ
					importance_l1_size = 200,
					importance_l2_size = 100,
					L2_reg = np.exp(-2))

train_params = dict(num_iters = 100,
					batch_size = 50,
					init_scale = np.exp(-4),
					step_size = np.exp(-6))

	
class Main(Chain):
	def __init__(self, model_params):
		initializer = chainer.initializers.HeNormal()
		super(Main, self).__init__(
			build_ecfp = Finger_print.ECFP(model_params),
			build_fcfp = Finger_print.FCFP(model_params),
			attension_layer1 = L.Linear(2 * model_params['fp_length'], model_params['importance_l1_size'],initialW=initializer),
			attension_layer2 = L.Linear(model_params['importance_l1_size'], model_params['importance_l2_size'],initialW=initializer),
			attension_layer3 = L.Linear(model_params['importance_l2_size'], 2 * model_params['fp_length'],initialW=initializer),
			dnn = Deep_neural_network.DNN(model_params),
		)
	
	def __call__(self, x, y):
		y = Variable(np.array(y, dtype=np.float32))
		pred = self.prediction(x)
		return F.mean_squared_error(pred, y)

	def prediction(self, x):
		x = Variable(x)
		ecfp = self.build_ecfp(x)
		fcfp = self.build_fcfp(x)
		ecfp_fcfp = F.concat((ecfp,fcfp),axis=1)

		h1 = self.attension_layer1(ecfp_fcfp)
		h2 = self.attension_layer2(h1)
		attention_vec = self.attension_layer3(h2)
		

		attention_vec_softmaxed = Variable(np.empty((attention_vec.shape), dtype=np.float32))
		for i in range(len(attention_vec)):
			attention_sum = F.sum(F.exp(attention_vec[i]))
			attention_sum_broadcasted = F.broadcast_to(attention_sum, (len(attention_vec[0]),))
			print("type ", attention_sum_broadcasted.dtype)
			print("shape ", attention_vec[i].shape)
			print("shape ", attention_vec_softmaxed[i].shape)
			attention_vec_softmaxed[i] = F.copy(attention_vec_softmaxed[i], F.exp(attention_vec[i]) /  attention_sum_broadcasted)

		#softmax_frac_broadcast = F.broadcast_to(softmax_frac, (len(attention_vec),len(attention_vec[0])))
		#attention_vec = F.exp(attention_vec) / softmax_frac_broadcast

		attentioned_ecfc = ecfp_fcfp * attention_vec

		pred = self.dnn(attentioned_ecfc)
		return pred

	def mse(self, x, y, undo_norm):
		y = Variable(np.array(y, dtype=np.float32))
		pred = undo_norm(self.prediction(x))
		return F.mean_squared_error(pred, y)
	
def train_nn(model, train_smiles, train_raw_targets, num_epoch=1000, batch_size=128, seed=0,
				validation_smiles=None, validation_raw_targets=None):

	train_targets, undo_norm = normalize_array(train_raw_targets)
	training_curve = []
	optimizer = optimizers.Adam()
	optimizer.setup(model)
	optimizer.add_hook(chainer.optimizer.WeightDecay(0.0001))	
	
	num_data = len(train_smiles)
	x = train_smiles
	y = train_targets
	sff_idx = npr.permutation(num_data)
	for epoch in range(num_epoch):
		epoch_time = time.time()
		for idx in range(0,num_data, batch_size):
			batched_x = x[sff_idx[idx:idx+batch_size
				if idx + batch_size < num_data else num_data]]
			batched_y = y[sff_idx[idx:idx+batch_size
				if idx + batch_size < num_data else num_data]]
			model.zerograds()
			loss = model(batched_x, batched_y)
			loss.backward()
			optimizer.update()
			#print("UPDATE TIME : ",  time.time() - update_time)
		#print "epoch ", epoch, "loss", loss._data[0]
		#print "epoch ", epoch, "loss", loss._data[0]
		if epoch % 100 == 0:
			train_preds = model.mse(train_smiles, train_raw_targets, undo_norm)
			cur_loss = loss._data[0]
			training_curve.append(cur_loss)
			print("Iteration", epoch, "loss", math.sqrt(cur_loss), \
				"train RMSE", math.sqrt((train_preds._data[0])))
			if validation_smiles is not None:
				validation_preds = model.mse(validation_smiles, validation_raw_targets, undo_norm)
				print("Validation RMSE", epoch, ":", math.sqrt((validation_preds._data[0])))
		#print("1 EPOCH TIME : ", time.time() - epoch_time)
		#print loss

		
	return model, training_curve, undo_norm

def main():
	print("Loading data...")
	#args
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file",type=str)
	parser.add_argument("--epochs", type=int)
	args = parser.parse_args()

	task_params = eval(args.input_file.split(".csv")[0]+'_params')
	ALL_TIME = time.time()
	traindata, valdata, testdata = load_data(
		task_params['data_file'], (task_params['train'], task_params['val'], task_params['test']),
		input_name = 'smiles', target_name = task_params['target_name'])
	x_trains, y_trains = traindata
	x_vals, y_vals = valdata
	x_tests, y_tests = testdata
	x_trains = np.reshape(x_trains, (task_params['train'], 1))
	y_trains = np.reshape(y_trains, (task_params['train'], 1))
	x_vals = np.reshape(x_vals, (task_params['val'], 1))
	y_vals = np.reshape(y_vals, (task_params['val'], 1))
	x_tests = np.reshape(x_tests, (task_params['test'], 1))
	y_tests = np.reshape(y_tests, (task_params['test'], 1)).astype(np.float32)

	def run_conv_experiment():
		'''Initialize model'''
		NNFP = Main(model_params) 
		optimizer = optimizers.Adam()
		optimizer.setup(NNFP)

		'''Learn'''
		trained_NNFP, conv_training_curve, undo_norm = \
			train_nn(NNFP, 
					 x_trains, y_trains,  
					 args.epochs,
					 validation_smiles=x_vals, 
					 validation_raw_targets=y_vals)
		return math.sqrt(trained_NNFP.mse(x_tests, y_tests, undo_norm)._data[0]), conv_training_curve

	print("Starting neural fingerprint experiment...")
	test_loss_neural, conv_training_curve = run_conv_experiment()
	print("Neural test RMSE", test_loss_neural)
	print("time : ", time.time() - ALL_TIME)
	#result_plot(conv_training_curve, train_params)

if __name__ == '__main__':
	main()
