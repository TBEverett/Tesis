#/bin/bash


instance=$1
ps=$2 #Population Size
gs=40 #Generation Size
ne=0.1 #Number of elite solutions
nc=0.1 #Number of neighbour solutions
lbd=0.1 #Lower Bound of Feasible Solutions
ubd=0.5 #Upper Bound of Feasible Solutions
t=5 #Max Runtime
s=42 #Seed

out=out.txt
ARGS="-i ${instance} -ps ${ps} -gs ${gs} -ne ${ne} -nc ${nc} -lbd ${lbd} -ubd ${ubd} -t ${t} -s ${s}"
screen=salida
rm -rf ${screen}

echo "./python3 SolveVRP.py ${ARGS} > ${screen}"
python3 SolveVRP.py ${ARGS} > ${screen}

quality=`tail -1 ${screen} |awk -F ' ' '{print $1}'`

echo "Quality: ${quality}"
