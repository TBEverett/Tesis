# Feature extractor for CVRPTW problem instances
# PENDING: Que funcione por directorio, creando un solo .csv

import pyvrp as p
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(prog="VRPFeatureExtractor",
                                 description="Produces metrics for VRP instance description")
parser.add_argument("-d", "--dir", required=True)
args = parser.parse_args()

def client_dist(A,B):
    return np.sqrt((A.y - B.y)**2 + (A.x - B.x)**2)
def dist(tuple1, tuple2):
    return np.sqrt((tuple1[0] - tuple2[0])**2 + (tuple1[1] - tuple2[1])**2)

# Funcion para obtener la maxima y minima cantidad de overlaps de ventanas de tiempo
# Este metodo de time sweep es extremadamente ineficiente, sería mejor sortear primero
# los comienzos y fines de las time windows y recorrerlos en orden, sumando al pasar por
# un comienzo y restando al pasar por un fin
def get_time_window_features(clients_list):
    time_windows_early = dict()
    time_windows_late = dict()
    overlaps = 0
    time_overlaps_dict = dict()
    window_lengths = list()
    for client in clients_list:
        if client.tw_late not in time_windows_late:
            time_windows_late[client.tw_late] = 0
        if client.tw_early not in time_windows_early:
            time_windows_early[client.tw_early] = 0
        time_windows_late[client.tw_late] += 1
        time_windows_early[client.tw_early] += 1
        window_lengths.append(client.tw_late - client.tw_early)
    max_time = max(time_windows_late) 
    for t in range(max_time):
        if t in time_windows_early:
            overlaps += time_windows_early[t]
        if t in time_windows_late:
            overlaps -= time_windows_late[t]
        time_overlaps_dict[t] = overlaps
    max_overlaps = max(list(time_overlaps_dict.values()))
    avg_overlaps = np.mean(list(time_overlaps_dict.values()))
    return {"max_overlaps": np.round(max_overlaps/len(clients),2), 
            "avg_overlaps": np.round(avg_overlaps/len(clients),2),
            "avg_window_length":np.round(np.mean(window_lengths)/max(window_lengths),2),
            "std_window_length":np.round(np.std(window_lengths)/max(window_lengths),2)}

features = dict()

#Leemos instancia y generamos modelo

dir = args.dir
instances = os.listdir(dir)
instances = [i for i in instances if ".txt" in i]

first_pass = True
for instance_name in instances:
    print("Extracting features for: ", instance_name)
    instance = p.read(dir+ "/" + instance_name, round_func="round", instance_format="solomon")
    model = p.Model.from_data(instance)

    #Construimos matriz de distancias (pyvrp ya trabaja con una interna pero no es facilmente accesible)
    clients = model._clients
    distance_matrix = [[] for client in clients]
    for i,client in enumerate(clients):
        for j,_client in enumerate(clients):
            distance_matrix[i].append(client_dist(client, _client))

    #Lista de features que hay que implementar:

    # DC1: Number of clients
    features["client_number"] = len(clients)

    # DC2: Depot Location (siempre hay 1 en las instancias)
    depot = (model._depots[0].x, model._depots[0].y)

    # ND3: Centroid of the nodes
    centroid = model.data().centroid()

    # DC3: Distance between centroid and depot
    features["distance_centroid_depot"] = dist(depot,centroid)

    # DC4: Average client distance to depot
    client_distances_to_depo = [dist((client.x,client.y),depot) for client in clients]
    features["average_distance_to_depot"] = np.mean(client_distances_to_depo)
    features["std_distance_to_depot"] = np.std(client_distances_to_depo)

    # DC5: Client Demands (Aqui no está claro a que se refiere el paper, se incluyeron 2 métricas)
    # DC5A: Standard Deviation of Client Demands
    all_demands = [client.demand for client in clients]
    features["standard_deviation_of_demands"] = np.std(all_demands)
    # DC5B: Mean of Client Demands
    features["mean_of_demands"] = np.mean(all_demands)

    # DC6: Ratio of total demand to total capacity
    capacity = model._vehicle_types[0].capacity
    features["ratio_total_demand_to_capacity"] = sum(all_demands)/capacity

    # DC9: Ratio between largest demand and capacity (todos los camiones tienen misma capacidad)
    largest_demand = max(all_demands)
    features["ratio_largest_demand_to_capacity"] = largest_demand/capacity

    # Extra: Ratio of median demand to capacity
    median_demand = np.median(all_demands)
    features["ratio_median_demand_to_capacity"] = median_demand/capacity

    # Extra: Number of vehicles
    features["number_of_vehicles"] = model.data().num_vehicles

    # DC10: Average number of clients per vehicle
    features["average_clients_per_vehicle"] = features["client_number"]/features["number_of_vehicles"]

    # ND4: Distance to centroid (Interpretado como Average Distance to Centroid y Standard Deviation of Distance to Centroid)
    # ND4A: Average Distance to Centroid
    distances_to_centroid = [dist(centroid,(c.x,c.y)) for c in clients]
    features["average_distance_to_centroid"] = np.mean(distances_to_centroid)
    # ND4B: Standard Deviation of Distance to Centroid
    features["std_of_distance_to_centroid"] = np.std(distances_to_centroid)

    # G1: Area of the enclosing rectangle
    max_x_value = max([client.x for client in clients])
    max_y_value = max([client.y for client in clients])
    min_x_value = min([client.x for client in clients])
    min_y_value = min([client.y for client in clients])
    features["area_enclosing_rectangle"] = (max_x_value - min_x_value) * (max_y_value - min_y_value)

    # Extra: Features de Time Windows
    time_window_features = get_time_window_features(clients)
    features["tw_max_overlaps"] = time_window_features["max_overlaps"]
    features["tw_avg_overlaps"] = time_window_features["avg_overlaps"]
    features["tw_avg_window_length"] = time_window_features["avg_window_length"]
    features["tw_std_window_length"] = time_window_features["std_window_length"]

    # Escribimos features a archivo de output
    if first_pass:
        f = open(dir + "_features.csv","a")
        f.write("instance,")
        for feature in features.keys():
            f.write(feature + ",")
        f.write("\n")
        first_pass = False
    f.write(instance_name + ",")
    for _,value in features.items():
        f.write(str(value) + ",")
    f.write("\n") 
f.close()





