import networkx as nx
import json
import time
import math
from collections import defaultdict
import copy
import os
import glob
# Constants
# MAX_DISTANCE = 50

start_time = time.time()
# Load network and benefits data
def load_data(network_file_path, benefits_file_path):
    with open(network_file_path, "r") as f:
        roads_data = json.load(f)
    with open(benefits_file_path, "r") as f:
        benefits_data = json.load(f)
    benefits_data = benefits_data[1:]   
    return roads_data, benefits_data

# Calculate distance between two coordinates
def calculate_distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def determine_maxspeed(highway_type, maxspeed_value):
    """Determine the maximum speed for a given road type and maxspeed value."""
    if maxspeed_value:
        if highway_type == "motorway":
            return 130
        try:
            return int(maxspeed_value)
        except ValueError:
            return 50  # Default value for unrecognized maxspeed
    else:
        if highway_type == "residential":
            return 50
        elif highway_type == "track":
            return 30
        else:
            return 100  # Default value for other highway types


def restructure_osm_data(osm_file, benefit_data):
    restructured_data = {}

    # Load OSM data
    with open(osm_file, "r") as f:
        osm_data = json.load(f)

    # Load benefit data
    

    for road in osm_data["features"]:
        if road['properties']['nodes']=='nan':
            continue
        road_id = str(road["properties"]["osmid"])
        highway_type = road["properties"].get("highway", "")
        maxspeed_value = road["properties"].get("maxspeed", None)

        # Initialize total_benefit with default values
        total_benefit = {str(i): 0 for i in range(1, 10)}

        # If the road has benefit data, update total_benefit
        if road_id in benefit_data:
            total_benefit.update(benefit_data[road_id].get("total_benefit", {}))

        road_data = {
            "id": road_id,
            "name": road["properties"].get("name", ""),
            "maxspeed": determine_maxspeed(highway_type, maxspeed_value),
            "is_oneway": 1 if road["properties"].get("oneway") in ["yes", "1", "true"] else 0,
            "highway_type": highway_type,
            "total_benefit": total_benefit,  
            "segments": {}
        }

        coordinates = road["geometry"]["coordinates"]
        
        for i in range(len(coordinates) - 1):
            segment_id = str(i + 1)
            segment_data = {
                "segment_start_id": road["properties"]["nodes"][i],
                "segment_end_id": road["properties"]["nodes"][i + 1],
                "segment_start_coordinate": coordinates[i],
                "segment_end_coordinate": coordinates[i + 1],
                "number_of_points": 0,
                "points": {},
                "benefit": {str(i): 0 for i in range(1, 10)}  # Default benefit values
            }

            # If benefit data exists for this road and segment, update benefit values
            if road_id in benefit_data and "segments" in benefit_data[road_id]:
                segment_benefits = benefit_data[road_id]["segments"].get(segment_id, {}).get("benefit", {})
                segment_data["benefit"].update(segment_benefits)
                segment_data["number_of_points"] = benefit_data[road_id]["segments"].get(segment_id, {}).get("number_of_points", 0)
                segment_data["points"] = benefit_data[road_id]["segments"].get(segment_id, {}).get("points", {})
            road_data["segments"][segment_id] = segment_data

        restructured_data[road_id] = road_data

    return restructured_data


# Build directed graph from roads data
def build_road_network(roads_data):
    road_network = nx.DiGraph()
    for road_id, road_data in roads_data.items():
        max_speed = road_data["maxspeed"]
        segments = road_data["segments"]
        is_oneway = road_data["is_oneway"]
        for segment_id, segment_info in segments.items():
            start = tuple(segment_info["segment_start_coordinate"])
            end = tuple(segment_info["segment_end_coordinate"])
            length = calculate_distance(start, end) / 1000  # in km
            time_cost = length / max_speed  # time = distance / speed
            benefit = segment_info["benefit"]
            class_id = int(max(benefit.items(), key=lambda x: x[1])[0])

            road_network.add_edge(start, end, road=road_id, segment=segment_id, benefit=benefit,
                                  distance=length, time_cost=time_cost, class_id=class_id)
            if not is_oneway:
                road_network.add_edge(end, start, road=road_id, segment=segment_id, benefit=benefit,
                                      distance=length, time_cost=time_cost, class_id=class_id)
    return road_network

# Is the segment valid?
def is_valid_segment(graph, node1, node2):
    return graph.has_edge(node1, node2)


class TimeoutException(Exception):
    pass

def run_astar_with_timeout(road_network, start, end, timeout=2):
    """Runs A* with a manual timeout using time.time()."""
    start_time = time.time()  # Start the timer

    try:
        # Run A* search but manually check for timeout
        for path in astar_generator(road_network, start, end):
            if time.time() - start_time > timeout:
                print("Timeout occurred.")
                return None  # Timeout happened, return None
            return path  # Return the found path immediately
    except nx.NetworkXNoPath:
        return None  # No path found

def astar_generator(road_network, start, end):
    """Generator function to allow manual timeout checking during A* search."""
    yield nx.astar_path(road_network, source=start, target=end, heuristic=calculate_distance, weight='distance')

# Example usage:
# path = run_astar_with_timeout(road_network, start, end, timeout=5)



def find_shortest_path_with_fallback(road_network, start_nodes, end_nodes, is_calculated, calculated_path, calculated_distance, timeout=5):
    """Finds the shortest path using A* with a fallback and timeout."""
    # Check cached results first
    for s, e in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        if is_calculated.get((start_nodes[s], end_nodes[e]), False):
            return calculated_path[start_nodes[s], end_nodes[e]], s, e

    shortest_path = None
    shortest_path_length = float('inf')
    s_true, e_true = None, None

    for s, e in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        start_0_added, start_1_added, end_0_added, end_1_added = False, False, False, False
        
        # Run A* with timeout
        path = run_astar_with_timeout(road_network, start_nodes[s], end_nodes[e], timeout)
        path_length = calculate_path_metrics(road_network, path)[0] if path else float('inf')
        # Skip if no path found or timeout occurred
        if path is None:
            continue

        # Adjust start and end if needed
        if s == 0 and (len(path) == 1 or path[1] != start_nodes[1]) and is_valid_segment(road_network, start_nodes[1], start_nodes[0]):
            path.insert(0, start_nodes[1])
            path_length += road_network[start_nodes[1]][start_nodes[0]]['distance']
            start_1_added = True
        elif s == 1 and (len(path) == 1 or path[1] != start_nodes[0]) and is_valid_segment(road_network, start_nodes[0], start_nodes[1]):
            path.insert(0, start_nodes[0])
            path_length += road_network[start_nodes[0]][start_nodes[1]]['distance']
            start_0_added = True

        if e == 0 and (len(path) == 1 or path[-2] != end_nodes[1]) and is_valid_segment(road_network, end_nodes[0], end_nodes[1]):
            path.append(end_nodes[1])
            path_length += road_network[end_nodes[0]][end_nodes[1]]['distance']
            end_1_added = True
        elif e == 1 and (len(path) == 1 or path[-2] != end_nodes[0]) and is_valid_segment(road_network, end_nodes[1], end_nodes[0]):
            path.append(end_nodes[0])
            path_length += road_network[end_nodes[1]][end_nodes[0]]['distance']
            end_0_added = True
        
        # Update shortest path if it's better
        if path_length < shortest_path_length:
            shortest_path_length = path_length
            shortest_path = path
            s_true, e_true = s, e

            # Adjust start/end flags
            if start_0_added:
                s_true = 0
            if start_1_added:
                s_true = 1
            if end_0_added:
                e_true = 0
            if end_1_added:
                e_true = 1

            # Cache the result
            is_calculated[start_nodes[s_true], end_nodes[e_true]] = True
            calculated_path[start_nodes[s_true], end_nodes[e_true]] = shortest_path
            calculated_distance[start_nodes[s_true], end_nodes[e_true]] = shortest_path_length

    return shortest_path, s_true, e_true





# Select top segments based on benefits and avoid problematic segments
def select_segments(benefits_data, problematic_segments, segment_number_per_class, total_number_of_classes):
    selected_segment_count = defaultdict(int)
    selected_segments = {}
    for i in range(1, total_number_of_classes + 1):
        selected_segment_count[i] = 0
    for data in benefits_data:
        class_id = data['class']
        if selected_segment_count[class_id] >= segment_number_per_class:
            continue
        start_id = data['segment_start_id']
        end_id = data['segment_end_id']
        if (start_id, end_id) in problematic_segments.values():
            continue
        
        # if any([start_id in values and end_id in values for values in problematic_segments.values()]):
        #     continue
        
        selected_segments[(start_id, end_id)] = data
        selected_segment_count[class_id] += 1
        if all(count >= segment_number_per_class for count in selected_segment_count.values()):
            break

    return selected_segments

def calculate_path_metrics(road_network, path):
    """Calculate total distance and time cost for a given path."""
    path_distance = 0
    path_time_cost = 0
    
    # Iterate over consecutive nodes in the path
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # Ensure the edge exists in the road network
        if road_network.has_edge(current_node, next_node):
            edge_data = road_network[current_node][next_node]
            path_distance += edge_data.get('distance', 0)  # Add distance
            path_time_cost += edge_data.get('time_cost', 0)  # Add time cost
        else:
            raise ValueError(f"No edge between {current_node} and {next_node} in the road network.")
    
    return path_distance, path_time_cost


# Calculate paths between selected segments
def calculate_paths(selected_segments, road_network, problematic_segments, no_path_count,no_path_count_per_id, total_number_of_classes,is_calculated,calculated_path,calculated_distance):
    all_paths = []
    is_wend=True
    no_path=False
    calculated_paths = []
    calculated_ids = []
    calculated_id_data = {}
    #no_path_count_per_id={}
    # problematic_segments = {}
    print('selected segments',len(selected_segments))
    i=1
    for (start_id, end_id), start_data in selected_segments.items():
        if (start_id,end_id) not in no_path_count_per_id.keys():
            no_path_count_per_id[(start_id,end_id)]=0
        start_nodes = [
            tuple(start_data["segment_start_coordinate"]),
            tuple(start_data["segment_end_coordinate"])
        ]
        start_class_id = start_data["class"]
        start_road_id = start_data["road_id"]
        start_segment_id = start_data["segment_id"]
        start_segment_benefit = start_data["benefit"]
        j=1
        for (end_start_id, end_end_id), end_data in selected_segments.items():
            if (end_start_id,end_end_id) not in no_path_count_per_id.keys():
                no_path_count_per_id[(end_start_id,end_end_id)]=0
            end_class_id  = end_data["class"]
            if (start_class_id == end_class_id) and (start_id == end_start_id) and (end_id == end_end_id):
                j+=1
                continue
            individual_path_time_start = time.time()
            end_nodes = [
                tuple(end_data["segment_start_coordinate"]),
                tuple(end_data["segment_end_coordinate"])
            ]
            
            end_road_id = end_data["road_id"]
            end_segment_id = end_data["segment_id"]
            end_segment_benefit = end_data["benefit"]

            # Find the shortest path with fallback
            shortest_path, s, e = find_shortest_path_with_fallback(road_network, start_nodes, end_nodes,is_calculated,calculated_path,calculated_distance)
            
            if not shortest_path:
                is_wend=False
                no_path=True
                if (start_id, end_id) or (end_start_id, end_end_id) not in problematic_segments:
                    no_path_count += 1
                    
                    
                    if i==1 and no_path_count_per_id[(start_id,end_id)]>=3:
                        
                        no_path_count_per_id[problematic_segments[no_path_count-1]]-=1
                        no_path_count_per_id[problematic_segments[no_path_count-2]]-=1
                        no_path_count_per_id[problematic_segments[no_path_count-3]]-=1
                        problematic_segments.pop(no_path_count-1)
                        problematic_segments.pop(no_path_count-2)
                        no_path_count-=3
                        problematic_segments[no_path_count] = (start_id, end_id)
                        no_path_count_per_id[(start_id,end_id)]+=1
                        print('abort for start segment c1, i=',i,'j=',j)
                        print('start_id',start_id,'end_id',end_id)
                        break
                    if i==1:
                        if j==2:
                            if start_segment_benefit>end_segment_benefit:
                                problematic_segments[no_path_count] = (end_start_id, end_end_id)
                                no_path_count_per_id[(end_start_id,end_end_id)]+=1
                                no_path_count_per_id[(start_id,end_id)]+=1
                                print('abort for end segment c1, i=',i,'j=',j)
                                print('start_id',start_id,'end_id',end_id)
                                print('end_start_id',end_start_id,'end_end_id',end_end_id)
                            else:
                                problematic_segments[no_path_count] = (start_id, end_id)
                                no_path_count_per_id[(start_id,end_id)]+=1
                                print('abort for start segment c2, i=',i,'j=',j)
                                print('start_id',start_id,'end_id',end_id)
                        else:
                            problematic_segments[no_path_count] = (end_start_id, end_end_id)
                            no_path_count_per_id[(end_start_id,end_end_id)]+=1
                            no_path_count_per_id[(start_id,end_id)]+=1
                            print('abort for end segment c2, i=',i,'j=',j)
                            print('start_id',start_id,'end_id',end_id)
                            print('end_start_id',end_start_id,'end_end_id',end_end_id)

                    else:
                        problematic_segments[no_path_count] = (end_start_id, end_end_id)
                        no_path_count_per_id[(end_start_id,end_end_id)]+=1
                        print('abort for end segment c3, i=',i,'j=',j)
                        print('start_id',start_id,'end_id',end_id)
                        print('end_start_id',end_start_id,'end_end_id',end_end_id)
                    # problematic_segments[no_path_count] = (start_id, end_id)
                abort_time = time.time()
                print(f"Abort time: {abort_time - individual_path_time_start:.2f} seconds")
                break
            
            if s==0:
                actual_start_id = start_id
                
            else:
                actual_start_id = end_id
                
            if e==0:
                actual_end_id=end_start_id
                
            else:
                actual_end_id=end_end_id
                
        
            # path_distance = nx.dijkstra_path_length(road_network, source=shortest_path[0], target=shortest_path[-1], weight='distance')
            # path_time_cost = nx.dijkstra_path_length(road_network, source=shortest_path[0], target=shortest_path[-1], weight='time_cost')
            
            path_distance, path_time_cost = calculate_path_metrics(road_network, shortest_path)
            
            if path_distance==0:
                print(actual_start_id, actual_end_id)
            # Calculate benefits
            benefits = {i: 0 for i in range(1, total_number_of_classes + 1)}
            benefits[start_class_id] += start_segment_benefit
            benefits[end_class_id] += end_segment_benefit
            if actual_start_id not in calculated_ids:
                calculated_ids.append(actual_start_id)
                calculated_id_data[actual_start_id] = start_data
                if actual_start_id==start_data['segment_start_id']:
                    calculated_id_data[actual_start_id]=copy.deepcopy(calculated_id_data[actual_start_id])
                    calculated_id_data[actual_start_id]['used'] = 'start'
                else:
                    calculated_id_data[actual_start_id]=copy.deepcopy(calculated_id_data[actual_start_id])
                    calculated_id_data[actual_start_id]['used'] = 'end'
                
            if actual_end_id not in calculated_ids:
                calculated_ids.append(actual_end_id)
                calculated_id_data[actual_end_id] = end_data
                if actual_end_id==end_data['segment_start_id']:
                    calculated_id_data[actual_end_id]=copy.deepcopy(calculated_id_data[actual_end_id])
                    calculated_id_data[actual_end_id]['used'] = 'start'
                else:
                    calculated_id_data[actual_end_id]=copy.deepcopy(calculated_id_data[actual_end_id])
                    calculated_id_data[actual_end_id]['used'] = 'end'
            calculated_paths.append((actual_start_id, actual_end_id))  # Fix: Use parentheses instead of square brackets
            all_paths.append({
                'start_road_id': start_road_id,
                "start_segment_id": start_segment_id,
                'actual_segment_start_id': actual_start_id,
                'end_road_id': end_road_id,
                "end_segment_id": end_segment_id,
                'actual_segment_end_id': actual_end_id,
                'number_of_segments': len(shortest_path),
                "distance": path_distance,
                "time": path_time_cost,
                "benefit": benefits,
                'start_segment_benefit': start_segment_benefit,
                'end_segment_benefit': end_segment_benefit,
                "path": shortest_path
            })
            print('path found, i=',i,'j=',j)
            individual_path_time_end = time.time()
            print(f"Individual path time: {individual_path_time_end - individual_path_time_start:.2f} seconds")
            j+=1
        i+=1
        if no_path:
            break
    return all_paths, problematic_segments, is_wend, no_path_count, calculated_paths,calculated_id_data,no_path_count_per_id,is_calculated,calculated_path,calculated_distance

# TODO: Calculate other paths
def calculate_other_paths(calculated_paths,road_network,all_paths,calculated_id_data,total_number_of_classes,is_calculated,calculated_path,calculated_distance):
    not_found_count=0
    for actual_start_id,start_data in calculated_id_data.items():
        if calculated_id_data[actual_start_id]['used']=='start':
            start_nodes = tuple(calculated_id_data[actual_start_id]["segment_start_coordinate"])
        else:
            start_nodes = tuple(calculated_id_data[actual_start_id]["segment_end_coordinate"]    )
        start_road_id = calculated_id_data[actual_start_id]["road_id"]
        start_segment_id = calculated_id_data[actual_start_id]["segment_id"]
        start_segment_benefit = calculated_id_data[actual_start_id]["benefit"]
        start_segment_class_id = calculated_id_data[actual_start_id]["class"]
        
        for actual_end_id, end_data in calculated_id_data.items():
            if actual_start_id==actual_end_id:
                continue
            if (actual_start_id, actual_end_id) in calculated_paths:
                continue
            if calculated_id_data[actual_end_id]['used']=='start':
                end_nodes = tuple(calculated_id_data[actual_end_id]["segment_start_coordinate"])
            else:
                end_nodes = tuple(calculated_id_data[actual_end_id]["segment_end_coordinate"])
            end_road_id = calculated_id_data[actual_end_id]["road_id"]
            end_segment_id = calculated_id_data[actual_end_id]["segment_id"]
            end_segment_benefit = calculated_id_data[actual_end_id]["benefit"]
            end_segment_class_id = calculated_id_data[actual_end_id]["class"]
            shortest_path=run_astar_with_timeout(road_network, start_nodes, end_nodes)
            benefits = {i: 0 for i in range(1, total_number_of_classes + 1)}
            if not shortest_path:
                path_distance=float('inf')
                path_time_cost=float('inf')
                start_segment_benefit=0
                end_segment_benefit=0
                not_found_count+=1
                print('no path found',not_found_count)
            else:
                path_distance=calculate_path_metrics(road_network,shortest_path)[0]
                path_time_cost=calculate_path_metrics(road_network,shortest_path)[1]
                benefits[start_segment_class_id] += start_segment_benefit
                benefits[end_segment_class_id] += end_segment_benefit
            all_paths.append({
                'start_road_id': start_road_id,
                "start_segment_id": start_segment_id,
                'actual_segment_start_id': actual_start_id,
                'end_road_id': end_road_id,
                "end_segment_id": end_segment_id,
                'actual_segment_end_id': actual_end_id,
                'number_of_segments': len(shortest_path),
                "distance": path_distance,
                "time": path_time_cost,
                "benefit": benefits,
                'start_segment_benefit': start_segment_benefit,
                'end_segment_benefit': end_segment_benefit,
                "path": shortest_path
            })
    return all_paths
# Main function
def path_finding(working_directory,segment_number_per_class, total_number_of_classes):
    start_time = time.time()
    workdir = os.path.join(os.getcwd(), working_directory)
    input_dir = os.path.join(workdir, "input")
    transient_dir = os.path.join(workdir, "transient")
    roads_data_file = os.path.join(transient_dir, "bc_benefits_output.json")
    benefits_data_file = os.path.join(transient_dir, "bc_top_benefits_output.json")
    roads_data, benefits_data = load_data(roads_data_file, benefits_data_file)
    osm_file=glob.glob(os.path.join(input_dir, '*.geojson'))
    osm_file=osm_file[0]
    osm_data=restructure_osm_data(osm_file,roads_data)
    road_network = build_road_network(osm_data)
    problematic_segments = {}
    is_wend=False
    no_path_count=0
    no_path_count_per_id={}

    is_calculated={}
    calculated_path={}
    calculated_distance={}
    while True:
        selected_segments = select_segments(benefits_data, problematic_segments, segment_number_per_class, total_number_of_classes)
        print('selected segments',len(selected_segments))
        all_paths, problematic_segments, is_wend, no_path_count, calculated_paths, calculated_id_data,no_path_count_per_id,is_calculated,calculated_path,calculated_distance = calculate_paths(selected_segments, road_network, problematic_segments, no_path_count,no_path_count_per_id, total_number_of_classes,is_calculated,calculated_path,calculated_distance)
        
        if is_wend:
            # calculated_id_data = [data for data in benefits_data if data['segment_start_id'] in calculated_ids or data['segment_end_id'] in calculated_ids]
            print('calculating other paths', no_path_count)
            all_paths=calculate_other_paths(calculated_paths,road_network,all_paths,calculated_id_data,total_number_of_classes,is_calculated,calculated_path,calculated_distance)
            path_calculation_end_time = time.time()
            print(f"Path calculation time: {path_calculation_end_time - start_time:.2f} seconds")
            print('done')
            break
        
        print('not done',no_path_count)
    # all_paths.append(selected_segments)
    write_path = os.path.join(transient_dir, "pf_output.json")
    write_output(write_path, all_paths)
    debug_path = os.path.join(transient_dir, "debug")
    with open(os.path.join(debug_path,'pf_output_tabbed.json'), 'w') as f:
        json.dump(all_paths, f, indent=4)
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
    print("Paths calculation completed.")

# Write output to JSON file
def write_output(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

# Run the main function
if __name__ == "__main__":
    path_finding(
        working_directory='work_dir/sample_data', #This is the working directory
        segment_number_per_class=2, #This is the number of segments per class
        total_number_of_classes=6, #This is the total number of classes
        )
