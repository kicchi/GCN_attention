#coding: utf-8
import math
import argparse
import copy
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import pylab
import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.offline as offline
#import cupy as np #GPUを使うためのnumpy
import chainer 
from chainer import cuda, Function, Variable, optimizers
from chainer import Link, Chain
from chainer import serializers
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
			 	 'train' : 2000,
			 	 'val' : 200,
			 	 'test' : 5000}
			 	 #'test' : 200}
malaria_params = {'target_name' : 'activity',
				'data_file'  : 'malaria.csv',
			 	 'train' : 1000,
			 	 'val' : 197,
			 	 'test' : 2000}

model_params = dict(fp_length = 50,      
					fp_depth = 4,       #NNの層と、FPの半径は同じ
					conv_width = 20,    #必要なパラメータはこれだけ（？）
					h1_size = 100,      #最上位の中間層のサイズ
					importance_l1_size = 100,
					importance_l2_size = 50,
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
			ecfp_attension_1 = L.Linear(model_params['fp_length'], model_params['importance_l1_size']),
			fcfp_attension_1 = L.Linear(model_params['fp_length'], model_params['importance_l1_size']),
			ecfp_attension_2 = L.Linear(model_params['importance_l1_size'], model_params['importance_l2_size']),
			fcfp_attension_2 = L.Linear(model_params['importance_l1_size'], model_params['importance_l2_size']),
			#ecfp_attension_3 = L.Linear(model_params['importance_l2_size'],1),
			#fcfp_attension_3 = L.Linear(model_params['importance_l2_size'],1),
			ecfp_attension_3 = L.Linear(model_params['importance_l2_size'],model_params['fp_length']),
			fcfp_attension_3 = L.Linear(model_params['importance_l2_size'],model_params['fp_length']),
			dnn = Deep_neural_network.DNN(model_params),
		)
	
	def __call__(self, x, y):
		y = Variable(np.array(y, dtype=np.float32))
		pred, _ = self.prediction(x)
		return F.mean_squared_error(pred, y)

	def prediction(self, x):
		x = Variable(x)
		#ecfp = self.build_ecfp(x)
		fcfp, input_attention = self.build_fcfp(x)
		#ecfp_beta = self.ecfp_attension(ecfp)
		#fcfp_beta = self.ecfp_attension(fcfp)
		#ecfp_beta = self.ecfp_attension_1(ecfp)
		#fcfp_beta = self.fcfp_attension_1(fcfp)
		#ecfp_beta = self.ecfp_attension_2(ecfp_beta)
		#fcfp_beta = self.fcfp_attension_2(fcfp_beta)
		#ecfp_beta = self.ecfp_attension_3(ecfp_beta)
		#fcfp_beta = self.fcfp_attension_3(fcfp_beta)
		
		#print("ecfp_beta : ",ecfp_beta[0])
		#print("F.exp(ecfp_beta) : ",F.exp(ecfp_beta[0]))
		#ecfp_alpha = F.exp(ecfp_beta) / (F.exp(ecfp_beta) + F.exp(fcfp_beta))
		#fcfp_alpha = F.exp(fcfp_beta) / (F.exp(ecfp_beta) + F.exp(fcfp_beta))
		#print("ecfp : ",ecfp.shape)
		#print("ecfp_alpha : ",ecfp.shape)
		#attension_ecfp = ecfp * ecfp_alpha
		#attension_fcfp = fcfp * fcfp_alpha
		#print("ecfp_alpha : ", F.mean(ecfp_alpha))
		#print("fcfp_alpha : ", F.mean(fcfp_alpha))

		#pred = self.dnn(attension_fcfp + attension_ecfp)
		pred = self.dnn(fcfp)
		return pred, input_attention

	def mse(self, x, y, undo_norm):
		y = Variable(np.array(y, dtype=np.float32))
		pred, input_attention = self.prediction(x)
		pred = undo_norm(pred)
		return F.mean_squared_error(pred, y), input_attention
	
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
			train_preds, _ = model.mse(train_smiles, train_raw_targets, undo_norm)
			cur_loss = loss._data[0]
			training_curve.append(cur_loss)
			print("Iteration", epoch, "loss", math.sqrt(cur_loss), \
				"train RMSE", math.sqrt((train_preds._data[0])))
			if validation_smiles is not None:
				validation_preds, _ = model.mse(validation_smiles, validation_raw_targets, undo_norm)
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
	parser.add_argument("--load_npz", type=str)
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

		#gpu_device = 0
		#cuda.get_device(gpu_device).use()
		#NNFP.to_gpu(gpu_device)
		'''Learn'''
		trained_NNFP, conv_training_curve, undo_norm = \
			train_nn(NNFP, 
					 x_trains, y_trains,  
					 args.epochs, 
					 validation_smiles=x_vals, 
					 validation_raw_targets=y_vals)
		save_name = "input_attention_one_hot_" + args.input_file + ".npz"
		serializers.save_npz(save_name, trained_NNFP)
		mse, _ = trained_NNFP.mse(x_tests, y_tests, undo_norm)
		return math.sqrt(mse._data[0]), conv_training_curve

	def load_model_experiment():
		'''Initialize model'''
		trained_NNFP = Main(model_params) 
		serializers.load_npz(args.load_npz, trained_NNFP)	
		_, undo_norm = normalize_array(y_tests)
		mse, input_attention = trained_NNFP.mse(x_tests, y_tests, undo_norm)
		return math.sqrt(mse._data[0]), input_attention

	print("Starting neural fingerprint experiment...")
	if args.load_npz == None:
		test_loss_neural, conv_training_curve = run_conv_experiment()
	else:
		test_loss_neural, input_attention = load_model_experiment()
		x_fcfp = input_attention._data[0]
		np.savetxt('fcfp_propaty_' + args.input_file,x_fcfp,delimiter=' ')
		np.set_printoptions(threshold=np.inf)

		def figure_histgram(weight):
			attentions = weight.T	
			hist_data = [attentions[i] + i for i in range(len(attentions))]
			group_labels = ['Donor', 'Acceptor', 'Aromatic', 'Halogen', 'Acidic', 'Basic']
			fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
			fig.update_layout(title_text='Da')
			#fig.show()

		figure_histgram(x_fcfp)

	print("Neural test RMSE", test_loss_neural)
	print("time : ", time.time() - ALL_TIME)
	#result_plot(conv_training_curve, train_params)

if __name__ == '__main__':
	main()
