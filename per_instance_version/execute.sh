#/bin/bash

seed=0 #Por ahora hardcodeado el seed, luego variable 
instance=$1
instance_group=$2
folder_name=$3

#Copiamos los contenidos de baseTuning
#Antes se copiaba todo baseTuning, pero ahora son muchos directorios, asi que es mejor
#copiar solo los archivos distintos para cada instancia (scn e inst)
baseDir="baseTuning"
newDir=${folder_name}/_${instance}_${baseDir}
mkdir ${newDir}
cp -r ${baseDir}/* ${newDir}/
cd ${newDir}

#Modificamos scn e inst para que trabajen sobre una sola instancia en particular
sed -i 's/solomon.inst/single.inst/' scn/SolveVRP.scn
echo ../../${instance_group}/${instance}.txt >> "inst/single.inst"

bash ToDoParamILS.sh toTune/SolveVRP.tune ${seed} _${instance}_${baseDir} > OUT
