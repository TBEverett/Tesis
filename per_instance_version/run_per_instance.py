import os
import subprocess
import threading

NTHREADS = 10

instance_group = "solomon" #o Homberger

#Obtenemos lista de instancias
instances_with_sols = os.listdir(instance_group)
instances = [file.replace(".txt","") for file in instances_with_sols if ".sol" not in file]
instance_amount_per_thread = len(instances)//NTHREADS


test = []
def threaded_paramILS(offset):
    for i in range(instance_amount_per_thread):
        #Ejecutamos paramILS, almacenando todo en un directorio para esa instancia
        if i + offset >= len(instances): #Caso para instancias finales
            break
        test.append(i + offset)
        subprocess.run(["bash","execute.sh",instances[i + offset],instance_group])

threads = list()
for thread_id in range(NTHREADS + 2):
    offset = thread_id*instance_amount_per_thread
    x = threading.Thread(target=threaded_paramILS, args=(offset,))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join() 

print("Todos los paramILS finalizaron su ejecución")