EPOCHS=2000
SAVEDIR=2019\_09\_24\_2

echo START
echo `date '+%y/%m/%d %H:%M:%S'`

for i in `seq 0 0`
do
python input_attention_one_hot_remove/chainer_regression_ecfp.py --input_file delaney.csv --epochs $EPOCHS > $SAVEDIR/input_attention_remove_worstg_ecfp_delaney_$i.txt
echo Exit fcfp  `date '+%y/%m/%d %H:%M:%S'`
python input_attention_one_hot_remove/chainer_regression_fcfp.py --input_file delaney.csv --epochs $EPOCHS > $SAVEDIR/input_attention_remove_worstg_fcfp_delaney_$i.txt
echo Exit fcfp  `date '+%y/%m/%d %H:%M:%S'`
done
