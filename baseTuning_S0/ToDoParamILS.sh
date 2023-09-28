#!/bin/bash

toTune=$1
seed=$2
maxEvaluations=1000
algo=SolveVRP

respaldos=respaldos${algo}
mkdir ${respaldos}

for function in $( cat ${toTune} ); do
	#crear archivo scenario y archivo parametros
        echo "hola"
	scenario=${function}.scn
        params=${function}.params
        instance=${function}.inst
	echo ${function}.params
        outputTuner=ParamILS_A${algo}_F${function}_S${seed}.out
        echo "outputTuner=ParamILS_A${algo}_F${function}_S${seed}.out"
        echo "time ruby paramils2.3.8-source/param_ils_2_3_run.rb -numRun ${seed} -approach focused -userunlog 1 -validN 0 -pruning 0 -maxEvals ${maxEvaluations} -scenariofile scn/${scenario} > ${outputTuner}"
        time ruby paramils2.3.8-source/param_ils_2_3_run.rb -numRun ${seed} -approach focused -userunlog 1 -validN 0 -pruning 0 -maxEvals ${maxEvaluations} -scenariofile scn/${scenario} > ${outputTuner}
        echo "mv out ${respaldos}/outA${algo}_F${function}_S${seed}"
        mv out ${respaldos}/outA${algo}_F${function}_S${seed}
	#done
        #mv ${scenario} ${params} ${instance} ${respaldos}
done

