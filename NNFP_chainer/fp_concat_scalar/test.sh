#python chainer_regression.py --input_file delaney.csv --epochs 10 --fp_length 25 --i 0 --load_npz fp_concat_delaney.csv_fp_length_25_None.npz 
#python chainer_regression_fig.py --input_file delaney.csv --epochs 10 --fp_length 25 --i 0 --load_npz fp_concat_malaria.csv_fp_length_25_0.npz 
#python chainer_regression.py --input_file cep.csv --epochs 100 --fp_length 25 --i 0 
#python chainer_regression.py --input_file malaria.csv --epochs 100 --fp_length 25 --i 0 --load_npz fp_concat_malaria.csv_fp_length_25_0.npz
#python chainer_regression.py --input_file cep.csv --epochs 10 --fp_length 25 --i 0 --load_npz fp_concat_cep.csv_fp_length_25.npz
#python chainer_regression.py --input_file cep.csv --epochs 100 --fp_length 25 --i 0 --load_npz test.npz
#python chainer_regression_fig.py --input_file delaney.csv --epochs 100 --fp_length 25 --i 0 --load_npz fig_delaney.csv.npz
python chainer_regression_fig.py --input_file malaria.csv --epochs 100 --fp_length 25 --i 0 --load_npz fig_delaney.csv.npz
#python chainer_regression_fig.py --input_file cep.csv --epochs 100 --fp_length 25 --i 0 --load_npz fig_cep.csv.npz
