#/bin/bash

seed=$1
baseDir="baseTuning"
newDir=S${seed}_${baseDir}
cp -r ${baseDir} ${newDir}
cd ${newDir}
nohup bash ToDoParamILS.sh toTune/SolveVRP.tune ${seed} > OUT &

