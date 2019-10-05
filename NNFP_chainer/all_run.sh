EPOCHS=1000
SAVEDIR=2019\_10\_05

echo START
echo `date '+%y/%m/%d %H:%M:%S'`

for i in `seq 0 0`
do
#python fp_concat_scalar/chainer_regression_fig.py --input_file delaney.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_fig_delaney_$i.txt
#echo Exit delaney `date '+%y/%m/%d %H:%M:%S'`
#python fp_concat_scalar/chainer_regression_fig.py --input_file malaria.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_fig_maralia_$i.txt
#echo Exit malaria `date '+%y/%m/%d %H:%M:%S'`
#python fp_concat_scalar/chainer_regression_fig.py --input_file cep.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_fig_cep_$i.txt
#echo Exit cep `date '+%y/%m/%d %H:%M:%S'`
python input_attention_one_hot/chainer_regression_ecfp.py --input_file delaney.csv --epochs $EPOCHS > $SAVEDIR/input_attention_ecfp_delaney.txt
echo Exit delaney `date '+%y/%m/%d %H:%M:%S'`
python input_attention_one_hot/chainer_regression_ecfp.py --input_file malaria.csv --epochs $EPOCHS > $SAVEDIR/input_attention_ecfp_malaria.txt
echo Exit malaria `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_top/chainer_regression_fcfp.py --input_file delaney.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_delaney_top.txt
#echo Exit delaney top `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_top/chainer_regression_fcfp.py --input_file malaria.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_malaria_top.txt
#echo Exit malaria top `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_top/chainer_regression_fcfp.py --input_file cep.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_cep_top.txt
#echo Exit cep top `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_worst/chainer_regression_fcfp.py --input_file malaria.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_malaria_worst.txt
#echo Exit malaria worst `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_worst/chainer_regression_fcfp.py --input_file cep.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_cep_worst.txt
#echo Exit cep worst `date '+%y/%m/%d %H:%M:%S'`
done
