import json
import time
import math
from operator import index
import random
import numpy as np
import os

start_time = time.time()
print('Start time is:', time.localtime())

class AntColony:
    def __init__(self, distance_matrix, time_matrix, benefit_matrix, all_keys, all_keys_benefit,n_ants, n_best, n_iterations, decay, alpha, beta, optimization_objective, time_limit):
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.benefit_matrix = benefit_matrix
        self.all_keys_benefit = all_keys_benefit
        self.all_keys_lookup = all_keys
        self.all_keys_list = list(all_keys)
        self.n_ants = n_ants
        self.n_best = n_best # this
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.time_limit = time_limit
        self.optimization_objective = optimization_objective
        self.pheromone = {key: 1 for key in self.distance_matrix.keys()}
        max_value = float('inf')
        min_value = float('-inf')
        #streamline normalizing the pheromone matrix!!!!!!!!!!!!!!!!!!
        if self.optimization_objective=='d': #for distance
            max_distance=max(value for value in self.distance_matrix.values() if value != max_value)
            self.normalized_distance = {key: value / max_distance for key, value in self.distance_matrix.items()}
            self.heuristic_info = {key: 1/value if value!=1 or value!=max_value else 1 for key, value in self.normalized_distance.items() }
        if self.optimization_objective=='t': #for time
            max_time=max(value for value in self.time_matrix.values() if value != max_value)
            self.normalized_time = {key: value / max_time for key, value in self.time_matrix.items()}
            self.heuristic_info = {key: 1/value if value!=1 or value!=max_value else 1 for key, value in self.normalized_time.items() } #for time
        if self.optimization_objective=='b': #for benefits
            max_benefit = max(value for value in self.benefit_matrix.values() if value != min_value)
            self.normalized_benefit = {key: value / max_benefit for key, value in self.benefit_matrix.items()}
            self.heuristic_info = {key: value if value!=min_value else 0 for key, value in self.normalized_benefit.items() if value!=min_value} #for benefits


    def run(self):
        shortest_path = None
        if self.optimization_objective=='d' or self.optimization_objective=='t':   #for distance, time
            all_time_shortest_path = ("placeholder", [float('inf'),float('inf'),float('-inf')])  #for distance, time
        else:
            all_time_shortest_path = ("placeholder", [float('inf'),float('inf'),float('-inf')]) #for benefits
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, shortest_path=shortest_path)
            if self.optimization_objective=='d': #for distance
                shortest_path=min(all_paths,key=lambda x: x[1][0])
                short_check = shortest_path[1][0]<all_time_shortest_path[1][0]
            if self.optimization_objective=='t': #for time
                shortest_path=min(all_paths,key=lambda x: x[1][1])
                short_check = shortest_path[1][1]<all_time_shortest_path[1][1]
            #shortest_path=min(all_paths,key=lambda x: x[1][1])  #for time
            if self.optimization_objective=='b': #for benefits
                shortest_path = max(all_paths, key=lambda x: x[1][2]) 
                short_check = shortest_path[1][2]>all_time_shortest_path[1][2]
            #index_of_min = min(enumerate(all_paths), key=lambda x: x[1][2])[0]
            
            if short_check:
                all_time_shortest_path = shortest_path
                #print(i,index_of_min)
                print(i)
                print(shortest_path)
            self.pheromone = self.evaporate_pheromone()
        return all_time_shortest_path

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path()
            if 0<len(path)<len(self.all_keys_list):
                i-=1
                continue
            all_paths.append((path, self.gen_path_cost(path)))
        return all_paths

    def gen_path(self):
        path = []
        start = random.choice(list(self.all_keys_list))
        path.append(start)
        while len(path) < len(self.all_keys_list):
            next_node = self.pick_next_node(path[-1], path)
            next_node=int(next_node)
            if next_node is None:
                path.append(next_node)
                break
            path.append(next_node)
        return path

    def pick_next_node(self, last_node, path):
        number_of_nodes = len(self.all_keys_list) + 1
        all_nodes = range(1, number_of_nodes)

        visited_nodes = set(path)
        unvisited_nodes = set(all_nodes) - visited_nodes

        if not unvisited_nodes:
            return None

        probabilities = []
        total = 0

        for node in unvisited_nodes:
            pheromone_level = self.pheromone.get((last_node, node), 0) ** self.alpha
            heuristic_level = self.heuristic_info.get((last_node, node), 0) ** self.beta
            prob = pheromone_level * heuristic_level
            probabilities.append((node, prob))
            total += prob

        if total == 0 or math.isnan(total):
            next_node = None
        else:
            probabilities = [(node, prob / total) for node, prob in probabilities]
            next_node = np.random.choice([node for node, prob in probabilities], p=[prob for node, prob in probabilities])
        return next_node

    def gen_path_cost(self, path):
        total_cost = 0
        total_time_cost = 0
        total_benefit = self.all_keys_benefit[path[0]]
        max_value = float('inf')
        min_value = float('-inf')
        for i in range(len(path) - 1):
            path_length = len(path)-1
            if self.distance_matrix[path[i], path[i + 1]] != max_value:
                total_cost += self.distance_matrix[path[i], path[i + 1]]
                total_time_cost += self.time_matrix[path[i], path[i + 1]]
                total_benefit += self.all_keys_benefit[path[i+1]]
                if total_time_cost>=self.time_limit:
                    total_time_cost-=self.time_matrix[path[i], path[i + 1]]
                    total_cost-=self.distance_matrix[path[i], path[i + 1]]
                    total_benefit-=self.benefit_matrix[path[i], path[i + 1]]
                    for j in range(i, path_length):
                        path.pop(-1)
                    break
        # if total_time_cost>self.time_limit:
        #     penalty_rate=0.99
        #     excess_time=total_time_cost-self.time_limit
        #     penalty=penalty_rate*excess_time
        #     if self.optimization_objective=='d': #for distance
        #         total_cost-=2*self.distance_matrix[path[i], path[i + 1]]
        #     if self.optimization_objective=='t': #for time
        #         total_time_cost-=2*self.time_matrix[path[i], path[i + 1]]
        #     if self.optimization_objective=='b': #for benefits
        #         total_benefit-=2*self.benefit_matrix[path[i], path[i + 1]] 
        return total_cost,total_time_cost,total_benefit

    def spread_pheromone(self, all_paths, shortest_path):
        if self.optimization_objective=='d': #for distance
            sorted_paths = sorted(all_paths, key=lambda x: x[1][0])
        if self.optimization_objective=='t': #for time
            sorted_paths = sorted(all_paths, key=lambda x: x[1][1])
        if self.optimization_objective=='b': #for benefits
            sorted_paths = sorted(all_paths, key=lambda x: x[1][2])
        
        for path, cost in sorted_paths[:self.n_best]:
            for i in range(len(path) - 1):
                if self.optimization_objective=='d': #for distance
                    self.pheromone[path[i], path[i + 1]] += self.normalized_distance[path[i], path[i + 1]]
                if self.optimization_objective=='t': #for time
                    self.pheromone[path[i], path[i + 1]] +=  self.normalized_time[path[i], path[i + 1]]
                if self.optimization_objective=='b': #for benefits
                    self.pheromone[path[i], path[i + 1]] +=  self.normalized_benefit[path[i], path[i + 1]]
    

    def evaporate_pheromone(self):
        return {key: (1 - self.decay) * pheromone for key, pheromone in self.pheromone.items()}

# Initialize the ant colony


def real_path_generation(shortest_path,path_matrix_index,optimization_objective,maxIter,antNo,time_limit,class_number):
    real_path = []
    for i, node in enumerate(shortest_path[0]):
        if i < len(shortest_path[0])-1:
            next_node = shortest_path[0][i+1]
        else:
            break
        if (node, next_node) in path_matrix_index:
            real_path.extend(path_matrix_index[node, next_node][:-1])
        #real_path.append(all_keys[node])
        real_path_distance=shortest_path[1][0]
        real_path_time=shortest_path[1][1]
        real_path_benefit=shortest_path[1][2]
    real_route={
        "Optimization Objective": optimization_objective,
        'Number of Iterations': maxIter,
        'Number of Ants': antNo,
        'Time Limit' : time_limit,
        'Class number': class_number,
        'Distance': real_path_distance,
        'Time': real_path_time,
        'Benefit': real_path_benefit,
        'Path': real_path,
        }
    
    return real_route

def data_preprocessing(network_file_path, number_of_classes):
    with open(network_file_path, "r") as f:
        network_data = json.load(f)
    distance_matrix = {}
    benefit_matrix = {}
    time_matrix = {}
    path_matrix = {}
    path_class_id = {}
    all_keys = {}
    distance_matrix_index = {}
    time_matrix_index = {}
    benefit_matrix_index = {}
    all_keys_benefit_index = {}
    path_matrix_index = {}
    node_count = {}
    path_count = {}
    path_classes = []
    segments_in_class_number = {}
    first_segment_class={}
    second_segment_class={}
    segments_by_benefit = {}
    all_keys_count = 0
    all_keys_benefit = {}
    
    for data in network_data:
        start_road_id = data['start_road_id']
        start_segment_id = data['start_segment_id']
        actual_start= data['actual_segment_start_id']
        end_road_id = data['end_road_id']
        end_segment_id = data['end_segment_id']
        actual_end= data['actual_segment_end_id']
        key1 = actual_start
        key2 = actual_end
        class_count = 0
        segments_by_benefit[actual_start, actual_end] = {}
        for class_id in range(1, number_of_classes+1):
            segments_in_class_number[class_id] = 0
        for key, value in data['benefit'].items():
            segments_by_benefit[actual_start, actual_end][int(key)] = value
            if value!=0:
                path_classes.append(int(key))
                segments_in_class_number[int(key)] += 1
                if class_count == 0:
                    first_segment_class[actual_start, actual_end] = int(key)
                    class_count += 1
                else:
                    second_segment_class[actual_start, actual_end] = int(key)
        check_key1 = key1 in  all_keys.values()
        check_key2 = key2 in all_keys.values()
        if (check_key1==False or check_key2==False):
            #node_count[class_id] += 1
            all_keys_count += 1
            if check_key1==False and check_key2==True:
                all_keys[all_keys_count] = key1
            elif check_key1==True and check_key2==False:
                all_keys[all_keys_count] = key2
            else:
                all_keys[all_keys_count] = key1
                #node_count[class_id] += 1
                all_keys_count += 1
                all_keys[all_keys_count] = key2
        # else:   
        #     if class_id in desired_class:
        #         path_count[class_id] += 1
            #continue
        distance = data['distance']
        time_cost = data['time']
        benefit = 0
        for _,value in data['benefit'].items():
            benefit+=value
        start_segment_benefit=data['start_segment_benefit']
        end_segment_benefit=data['end_segment_benefit']
        #path_class_id[key1, key2] = data['path_class_id']
        path= data['path']
        path_matrix[key1, key2] = path
        distance_matrix[key1, key2] = distance
        benefit_matrix[key1, key2] = benefit
        time_matrix[key1, key2] = time_cost
        all_keys_benefit[key1]=start_segment_benefit
        all_keys_benefit[key2]=end_segment_benefit
    # sum_path = 0
    # sum_node = 0
    # sum_path = len(path_class_id)
    # for class_id in desired_class:
    #     #path_count[class_id] += node_count[class_id]
    #     sum_path += path_count[class_id]
    #     sum_node += node_count[class_id]
    inverse_all_keys = {v: k for k, v in all_keys.items()}
    for data in network_data:
        # class_id = data['path_class_id']
        # if class_id not in desired_class:
        #     continue
        start_road_id = data['start_road_id']
        start_segment_id = data['start_segment_id']
        actual_start= data['actual_segment_start_id']
        end_road_id = data['end_road_id']
        end_segment_id = data['end_segment_id']
        actual_end= data['actual_segment_end_id']
        key1 = actual_start
        key2 = actual_end
        if key1 in inverse_all_keys and key2 in inverse_all_keys:
            index1 = inverse_all_keys[key1]
            index2 = inverse_all_keys[key2]
            distance_matrix_index[index1, index2] = distance_matrix[key1, key2]
            time_matrix_index[index1, index2] = time_matrix[key1, key2]
            benefit_matrix_index[index1, index2] = benefit_matrix[key1, key2]
            path_matrix_index[index1, index2] = path_matrix[key1, key2]
            all_keys_benefit_index[index1]=all_keys_benefit[key1]
            all_keys_benefit_index[index2]=all_keys_benefit[key2]

    matrix_size = len(inverse_all_keys) + 1
    max_value = float('inf')
    min_value = float('-inf')
    for i in range(1, matrix_size):
        for j in range(1, matrix_size):
            if (i, j) not in distance_matrix_index or distance_matrix_index[i, j] == 1e+20:
                distance_matrix_index[i, j]=max_value
            if (i, j) not in time_matrix_index or time_matrix_index[i, j] == 1e+20:
                time_matrix_index[i, j]=max_value
            if (i, j) not in benefit_matrix_index or benefit_matrix_index[i, j] == -6e+20:
                benefit_matrix_index[i, j]=min_value
            if (i, j) not in path_matrix_index:
                path_matrix_index[i, j] = []
    #print('All keys:', all_keys)
    # graph becomes disconnected using one way streets
    incidence_matrix = np.zeros((matrix_size, matrix_size))
    for i in range(1, matrix_size):
        for j in range(1, matrix_size):
            if distance_matrix_index[i, j] != max_value:
                incidence_matrix[i, j] = 1
    return distance_matrix_index, time_matrix_index, benefit_matrix_index, path_matrix_index, all_keys, all_keys_benefit_index, matrix_size, max_value, min_value
    
def route_finding(working_directory, number_of_classes, time_limit, optimization_objective, max_iter, ant_no):
    
    workdir = os.path.join(os.getcwd(), working_directory)
    transient_dir=os.path.join(workdir, "transient")
    network_file_path = os.path.join(transient_dir, "pf_output.json")
    write_file_path = os.path.join(transient_dir, "solution.json")
    maxIter = max_iter
    antNo = ant_no
    rho = 0.5  # Evaporation rate, [0, 1), default=0.5, best so far=0.5
    alpha = 0.25 # Pheromone factor, >=0, default=1, best so far=0.35
    beta = 5  # Attractiveness factor, >0, default=1, best so far>=1
    # beta>>alpha for best results

    distance_matrix, time_matrix, benefit_matrix, path_matrix, all_keys, all_keys_benefit, matrix_size, max_value, min_value = data_preprocessing(network_file_path, number_of_classes)
    colony = AntColony(distance_matrix, time_matrix, benefit_matrix,all_keys,all_keys_benefit, n_ants=antNo, n_best=5, n_iterations=maxIter, decay=rho, alpha=alpha, beta=beta, optimization_objective=optimization_objective, time_limit=time_limit)
    # Run the optimization
    shortest_path = colony.run()
    real_route = real_path_generation(shortest_path, path_matrix, optimization_objective, maxIter, antNo, time_limit, number_of_classes)
    # with open(write_file_path, "w") as f:
    #     json.dump(real_route, f, indent=4)
    # debug_path=os.path.join(transient_dir, "debug")
    with open(write_file_path, "w") as f:
        json.dump(real_route, f, indent=4)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    execution_time_minutes = execution_time / 60
    print("Execution time:", execution_time_minutes, "minutes")
    print("done")
    return shortest_path


if __name__ == "__main__":
    route_finding(
        working_directory='work_dir/magdeburg15',
        number_of_classes=15,
        time_limit=80,
        optimization_objective='d',
        max_iter=500,
        ant_no=50
    )