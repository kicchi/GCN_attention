EPOCHS=2000
SAVEDIR=2019\_09\_24

echo START
echo `date '+%y/%m/%d %H:%M:%S'`

for i in `seq 0 0`
do
python fp_concat_scalar/chainer_regression.py --input_file delaney.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_delaney_$i.txt
python fp_concat_scalar/chainer_regression.py --input_file malaria.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_maralia_$i.txt
python fp_concat_scalar/chainer_regression.py --input_file cep.csv --epochs $EPOCHS --fp_length 25 --i $i > $SAVEDIR/fp_concat_scalar_cep_$i.txt
#python input_attention_one_hot_remove/chainer_regression_ecfp.py --input_file malaria.csv --epochs $EPOCHS > $SAVEDIR/input_attention_ecfp_malaria_remove_top_$i.txt
echo Exit ecfp  `date '+%y/%m/%d %H:%M:%S'`
#python input_attention_one_hot_remove/chainer_regression_fcfp.py --input_file malaria.csv --epochs $EPOCHS > $SAVEDIR/input_attention_fcfp_malaria_remove_top_$i.txt
echo Exit fcfp  `date '+%y/%m/%d %H:%M:%S'`
done
