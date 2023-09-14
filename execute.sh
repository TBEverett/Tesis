#/bin/bash

seed=$1
baseDir="baseTuning"
newDir=${baseDir}_S${seed}
cp -r ${baseDir} ${newDir}
cd ${newDir}
nohup bash ToDoParamILS.sh toTune/SolveVRP.tune ${seed} > OUT &

