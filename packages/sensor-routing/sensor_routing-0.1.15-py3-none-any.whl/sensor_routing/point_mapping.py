import json
from shapely import Point, STRtree, box
import math
import time
import os
import glob
import pandas as pd

def convert_to_csv(working_directory):
    workdir = working_directory
    input_dir = os.path.join(workdir, "input")
    input_files = glob.glob(os.path.join(input_dir, '*.txt'))  # Get list of txt files

    if not input_files:
        print("No input files found.")
        return None

    input_file = input_files[0]  # Assuming there's only one .txt file
    output_file = os.path.join(input_dir, "converted.csv")

    # Read the text file
    with open(input_file, "r") as f:
        lines = f.readlines()

    if not lines:
        print("Input file is empty.")
        return None

    # Process data
    data = []
    for line in lines:
        values = line.split()  # Split by whitespace
        if len(values) < 3:  # Ensure there are at least Easting, Northing, and 1 cluster
            continue
        
        easting, northing = values[:2]  # First two columns
        clusters = values[2:]  # Everything else is a cluster
        row = [easting, northing] + clusters
        data.append(row)

    # Dynamically count clusters
    num_clusters = len(data[0]) - 2  # Subtracting Easting & Northing
    columns = ["Easting", "Northing"] + [f"Cluster{i+1}" for i in range(num_clusters)]

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Save to CSV
    df.to_csv(output_file, index=False)

    print(f"CSV file saved as {output_file}")
    return output_file


def distance_point_to_segment(point, segment_start, segment_end):
    def dot(v, w):
        return v[0] * w[0] + v[1] * w[1]

    def length_sq(v):
        return v[0] ** 2 + v[1] ** 2

    def distance_sq_point_to_line(point, line_start, line_end):
        line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
        point_vec = (point[0] - line_start[0], point[1] - line_start[1])
        proj_length = dot(point_vec, line_vec) / length_sq(line_vec)

        if proj_length < 0:
            return length_sq(point_vec)
        elif proj_length > 1:
            return length_sq((point[0] - line_end[0], point[1] - line_end[1]))
        else:
            proj_point = (
                line_start[0] + proj_length * line_vec[0],
                line_start[1] + proj_length * line_vec[1],
            )
            return length_sq((point[0] - proj_point[0], point[1] - proj_point[1]))

    return math.sqrt(distance_sq_point_to_line(point, segment_start, segment_end))

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

def point_mapping(
    working_directory, min_distance_to_road,is_reversed 
):
    workdir = working_directory
    input_dir = os.path.join(workdir, "input")
    transient_dir = os.path.join(workdir, "transient")
    geojson_files = glob.glob(os.path.join(input_dir, '*.geojson'))
    road_information_path = next((f for f in geojson_files if '_4326' not in f), None)
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    if not csv_files:
        csv_files = convert_to_csv(working_directory)
    else:
        csv_files = csv_files[0]
    point_information_path = csv_files
    start_time = time.time()
    # print("Start time is:", time.localtime())

    # Load point information and initialize STRtree
    marker_classification = {}
    markers = []
    with open(point_information_path, "r") as f:
        next(f)  # Skip header
        for line in f:
            line.strip()
            # classification = [float(c) for c in line.split("   ")[3:]]
            if line.split(",")[2] == '':
                continue
            classification = [float(c) for c in line.split(",")[2:]]
            if 0.9999 > sum(classification) > 1:
                print("Error: ", classification)
                continue
            # for entry in line[3:]:
            #     print(entry)
            # x_string=line.split('   ')[1]
            x, y = float(line.split(",")[0]), float(line.split(",")[1]) #correct easting northing
            if is_reversed:
                x,y = y,x
            # y,x = x,y #reversed
            markers.append(Point(x, y))
            marker_classification[(x, y)] = classification

    str_tree = STRtree(markers)

    # Load road information and process each road
    roads = {}
    
    road_types = [
        "motorway",
        "trunk",
        "primary",
        "secondary",
        "tertiary",
        "unclassified",
        "motorway_link",
        "trunk_link",
        "primary_link",
        "secondary_link",
        "tertiary_link",
        "residential",
        "track",
        'living_street',
    ]
    with open(road_information_path, "r") as f:
        data = json.load(f)
        global_x_min = math.inf
        global_y_min = math.inf
        global_x_max = -math.inf
        global_y_max = -math.inf
        for feature in data["features"]:
            access_information= feature["properties"].get("access", None)
            is_accessible= 1 if access_information == "yes" or access_information is None else 0
            if feature["geometry"]["type"] == "LineString" and feature["properties"]["highway"] in road_types and is_accessible==1:
                road_id = int(feature["properties"]["osmid"])

                # Check if this road is indicated as a one-way
                # is_oneway = 1 if road_id in oneway_ids else 0
                oneway_information= feature["properties"].get("oneway", None)
                
                way_points = feature["geometry"]["coordinates"]
                segment_nodes = feature["properties"]["nodes"]
                highway_type = feature["properties"]["highway"]
                road_name = feature["properties"]["name"]
                maxspeed = feature["properties"].get("maxspeed", None)
                maxspeed = determine_maxspeed(highway_type, maxspeed)
                maxspeed = int(maxspeed)
                is_oneway= 1 if oneway_information == "yes" else 0
                

                # Update global bounding box
                x_min = min([x for x, y in way_points])
                y_min = min([y for x, y in way_points])
                x_max = max([x for x, y in way_points])
                y_max = max([y for x, y in way_points])
                global_x_min = min(global_x_min, x_min)
                global_y_min = min(global_y_min, y_min)
                global_x_max = max(global_x_max, x_max)
                global_y_max = max(global_y_max, y_max)

                # Query STRtree for points within min_distance_to_road
                indices = str_tree.query(box(x_min, y_min, x_max, y_max), predicate="dwithin", distance=min_distance_to_road)

                points_covered = [(str_tree.geometries[index].x, str_tree.geometries[index].y) for index in indices]
                if points_covered:
                    roads[road_id] = [
                        way_points,
                        (x_min, y_min, x_max, y_max),
                        segment_nodes,
                        highway_type,
                        road_name,
                        maxspeed,
                        is_oneway,
                        is_accessible,
                        points_covered,
                    ]

    # Further processing to calculate distances and create structured data
    segment_point_count = {}
    structured_data = {}
    min_distances = {}
    max_distance_to_segment = min_distance_to_road

    for road_id, road_data in roads.items():
        way_points, _, segment_nodes, _, _, _, _, _, _ = road_data
        segment_point_count[road_id] = {}
        for i in range(len(way_points) - 1):
            segment_key = i + 1
            segment_point_count[road_id][segment_key] = 0
            lp1 = way_points[i]
            lp2 = way_points[i + 1]
            for p in road_data[-1]:
                act_dist = distance_point_to_segment(p, lp1, lp2)
                if road_id not in min_distances:
                    min_distances[road_id] = {}
                if segment_key not in min_distances[road_id]:
                    min_distances[road_id][segment_key] = {}
                if act_dist <= max_distance_to_segment:
                    segment_point_count[road_id][segment_key] += 1
                    min_distances[road_id][segment_key][segment_point_count[road_id][segment_key]] = {
                        "point_coordinates": p,
                        "distance_to_segment": act_dist,
                        "membership_values": marker_classification[p],
                        "class": marker_classification[p].index(
                            max(marker_classification[p])
                        )
                        + 1,
                    }

    for road_id, road_data in roads.items():
        (
            way_points,
            bounding_box,
            segment_nodes,
            highway_type,
            road_name,
            maxspeed,
            is_oneway,
            is_accessible,
            points_covered,
        ) = road_data
        road_id = int(road_id)
        if road_id in min_distances:
            structured_data[road_id] = {
                "id": road_id,
                "name": road_name,
                "maxspeed": maxspeed,
                "is_oneway": is_oneway,
                "is_accessible": is_accessible,
                "highway_type": highway_type,
                "segments": {},
            }
        else:
            continue

        for i in range(len(way_points) - 1):
            segment_key = i + 1
            lp1 = way_points[i]
            lp2 = way_points[i + 1]
            segment_data = {
                "segment_start_id": segment_nodes[i],
                "segment_end_id": segment_nodes[i + 1],
                "segment_start_coordinate": [lp1],
                "segment_end_coordinate": [lp2],
                "number_of_points": segment_point_count[road_id][segment_key],
                "points": (
                    min_distances[road_id][segment_key]
                    if segment_key in min_distances[road_id]
                    else {}
                ),
            }

            segment_data["number_of_points"] = segment_point_count[road_id][segment_key]
            if segment_data["points"] == {}:
                segment_data.pop("points")
                segment_data["number_of_points"] = 0
            structured_data[road_id]["segments"][segment_key] = segment_data
    os.makedirs(transient_dir, exist_ok=True)
    write_file_path = os.path.join(transient_dir, "pm_output.json")
    # Save to file
    with open(write_file_path, "w") as f:
        json.dump(structured_data, f)
    #for checking
    debug_dir = os.path.join(transient_dir, "debug")
    os.makedirs(debug_dir, exist_ok=True)
    with open(os.path.join(debug_dir,"pmo_debug_tabbed.json"), "w") as f:
        json.dump(structured_data, f, indent=4)

    end_time = time.time()
    execution_time = end_time - start_time
    # print("Execution time:", execution_time, "seconds")
    # print("Execution time:", execution_time / 60, "minutes")
    # print("done")
    return len(classification)


if __name__ == "__main__":
    
    working_directory = 'work_dir/sample_data'
    is_reversed = True
    point_mapping(
        working_directory,
        50, # This is the maximum distance to the road
        is_reversed
    )