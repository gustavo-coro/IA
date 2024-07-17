NUM_RUNS=10

FILE_ENTRADA="instancia"
DATA_FILE="testes/$FILE_ENTRADA/teste_melhor.txt"
POPULACAO=150
ITERACOES=200
C1=0.9
C2=1.5

printf "$POPULACAO\n$ITERACOES\n$C1\n$C2\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python tsp_pso.py $FILE_ENTRADA.txt $POPULACAO $ITERACOES $C1 $C2
done