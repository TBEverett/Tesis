import os
import subprocess

instance_group = "solomon" #o Homberger

#Obtenemos lista de instancias
instances_with_sols = os.listdir(instance_group)
instances = [file.replace(".txt","") for file in instances_with_sols if ".sol" not in file]

for instance in instances:
    #Ejecutamos paramILS, almacenando todo en un directorio para esa instancia
    subprocess.run(["bash","execute.sh",instance,instance_group])
