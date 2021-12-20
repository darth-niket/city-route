#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
from numpy import float64
import pandas as pd
from math import radians, cos, sin, asin, sqrt, tanh
import heapq




def successors(curr_city,roadSegments):
    return roadSegments[(roadSegments['source']== curr_city) | (roadSegments['destination']== curr_city)]

def routes_structure(route,roadSegments):
    route_taken=[]
    for i in range(0,len(route)-1):
        j= i+1
        row = roadSegments[(roadSegments['source'] == route[i]) & (roadSegments['destination']== route[j])]
       
        if(len(row)== 0 ):
                    row = roadSegments[(roadSegments['destination']== route[i]) & (roadSegments['source']== route[j])]
        new_tuple=(route[i+1],str(row['name_of_highway'].to_string(index=False))+" for "+ str(row['distance'].to_string(index=False))+" miles")
        
        route_taken.append(new_tuple)

    return route_taken




def optimum_segments(start,end,roadSegments,cityGps):
    
    visited_fringe = []
    segments = 0
    total_miles = 0
    total_delivery_hours = 0
    total_miles = 0
    path = start
    distance = 0
    priority = 0
    fringe = [(segments,start, total_miles, total_miles, total_delivery_hours, path)]
    heapq.heapify(fringe)

    while fringe:

        (segments,curr_city, total_miles, total_hours, total_delivery_hours, path) = heapq.heappop(fringe)
    
        if curr_city == end:
            break
        if curr_city in visited_fringe:
            continue
        visited_fringe.append(curr_city)
        prev_city = curr_city


        nearest_cities=successors(curr_city,roadSegments)
        segments += 1

        h_fringe = []
        for index, row in nearest_cities.iterrows():

             visited_check_list =[]
             if row['speedlimit'] >= 50 and row not in visited_check_list:
                
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']
                t_road = t_road + tanh(row['distance']/1000) * 2 *(t_road + t_trip)
             else:
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']

             if row['destination'] == curr_city:
                 source = cityGps[cityGps['city'] == row['destination']]
                 destination = cityGps[cityGps['city'] == row['source']]
                 cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                 heapq.heappush(fringe,[segments ,row['source'], total_miles + row['distance'],total_hours + (row['distance']/row['speedlimit']), t_trip +t_road ,path +" "+ row['source']])
   
             else:
                source = cityGps[cityGps['city'] == curr_city]
                destination = cityGps[cityGps['city'] == row['destination']]
                cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                heapq.heappush(fringe,[segments,row['destination'], total_miles + row['distance'],total_hours + (row['distance']/row['speedlimit']),t_trip +t_road ,path+ " "+ row['destination']])
 

    routes= path.split(" ")

    route_taken = routes_structure(routes,roadSegments)
 
    return {"total-segments" : segments, 
            "total-miles" : float(total_miles), 
            "total-hours" : float(total_hours), 
            "total-delivery-hours" : float(total_delivery_hours), 
            "route-taken" : route_taken }
    

def optimum_distance(start,end,roadSegments,cityGps):
    
    
    visited_fringe = []
    segments = 0
    total_miles = 0
    total_delivery_hours = 0
    total_miles = 0
    path = start
    distance = 0
    priority = 0
    
    fringe = [(priority,start, segments, total_miles, total_miles, total_delivery_hours, path)]
    heapq.heapify(fringe)

    while fringe:

        (priority,curr_city, segments, total_miles, total_hours, total_delivery_hours, path) = heapq.heappop(fringe)
    
        if curr_city == end:
            break
        if curr_city in visited_fringe:
            continue
        visited_fringe.append(curr_city)
        prev_city = curr_city

        nearest_cities=successors(curr_city,roadSegments)
        segments += 1

        h_fringe = []
        for index, row in nearest_cities.iterrows():

             visited_check_list =[]
             if row['speedlimit'] >= 50 and row not in visited_check_list:
                
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']
                t_road = t_road + tanh(row['distance']/1000) * 2 *(t_road + t_trip)
             else:
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']

            

             if row['destination'] == curr_city:
                 source = cityGps[cityGps['city'] == row['destination']]
                 destination = cityGps[cityGps['city'] == row['source']]
                 cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                 heapq.heappush(fringe,[priority + row['distance']+ (cost/(segments*10)),row['source'],segments, total_miles + row['distance'], total_hours + ( row['distance']/row['speedlimit']), t_trip + t_road ,path +" "+ row['source']])
   
             else:
                source = cityGps[cityGps['city'] == curr_city]
                destination = cityGps[cityGps['city'] == row['destination']]
                cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                heapq.heappush(fringe,[priority + row['distance']+(cost/(segments*10)),row['destination'],segments, total_miles + row['distance'], total_hours + (row['distance']/row['speedlimit']), t_trip + t_road ,path+ " "+ row['destination']])
 

    routes= path.split(" ")

    route_taken= routes_structure(routes,roadSegments)

    return {"total-segments" : segments, 
            "total-miles" : float(total_miles), 
            "total-hours" : float(total_hours), 
            "total-delivery-hours" : float(total_delivery_hours), 
            "route-taken" : route_taken }

def optimum_time(start,end,roadSegments,cityGps, maxspeed):

    visited_fringe = []
    segments = 0
    total_miles = 0
    total_delivery_hours = 0
    total_hours = 0
    path = start
    priority = 0
    fringe = [(priority,start, segments, total_miles, total_hours, total_delivery_hours, path)]
    heapq.heapify(fringe)

    while fringe:

        (priority,curr_city, segments, total_miles, total_hours, total_delivery_hours, path) = heapq.heappop(fringe)

        
        if curr_city == end:
            break
        if curr_city in visited_fringe:
            continue
        visited_fringe.append(curr_city)
        prev_city = curr_city

        nearest_cities=successors(curr_city,roadSegments)
        segments += 1

        h_fringe = []
        for index, row in nearest_cities.iterrows():

             visited_check_list =[]
             if row['speedlimit'] >= 50 and row not in visited_check_list:
                
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']
                t_road = t_road + tanh(row['distance']/1000) * 2 *(t_road + t_trip)
             else:
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']

             priority += 1
             if row['destination'] == curr_city:
                 source = cityGps[cityGps['city'] == row['destination']]
                 destination = cityGps[cityGps['city'] == row['source']]
                 cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                 heapq.heappush(fringe,[total_hours + ( row['distance']/row['speedlimit']) + cost/(maxspeed*5),row['source'],segments, total_miles + row['distance'], total_hours + ( row['distance']/row['speedlimit']), t_road + t_trip,path +" "+ row['source']])

             else:
                source = cityGps[cityGps['city'] == curr_city]
                destination = cityGps[cityGps['city'] == row['destination']]
                cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                heapq.heappush(fringe,[total_hours + ( row['distance']/row['speedlimit']) + cost/(maxspeed*5) ,row['destination'],segments, total_miles + row['distance'], total_hours + (row['distance']/row['speedlimit']), t_road + t_trip ,path+ " "+ row['destination']])


    route= path.split(" ")

    route_taken = routes_structure(route,roadSegments)

    return {"total-segments" : segments, 
            "total-miles" : float(total_miles), 
            "total-hours" : float(total_hours), 
            "total-delivery-hours" : float(total_delivery_hours), 
            "route-taken" : route_taken }


def optimum_delivery_time(start,end,roadSegments,cityGps,maxspeed):

    visited_fringe = []
    segments = 0
    total_miles = 0
    total_delivery_hours = 0
    total_hours = 0
    path = start
    priority = 0
    fringe = [(total_hours,start, segments, total_miles, total_hours, total_delivery_hours, path)]
    heapq.heapify(fringe)

    while fringe:

        (total_hours,curr_city, segments, total_miles, total_hours, total_delivery_hours, path) = heapq.heappop(fringe)
    
        if curr_city == end:
            break
        if curr_city in visited_fringe:
            continue
        visited_fringe.append(curr_city)
        prev_city = curr_city

        nearest_cities=successors(curr_city,roadSegments)
        segments += 1

        h_fringe = []
        for index, row in nearest_cities.iterrows():


             visited_check_list =[]
             if row['speedlimit'] >= 50 and row not in visited_check_list:
                 visited_check_list.append(row)
                 t_trip = total_delivery_hours
                 t_road = row['distance']/row['speedlimit']
                 t_road = t_road + tanh(row['distance']/1000) * 2*(t_road + t_trip)
             else:
                t_trip = total_delivery_hours
                t_road = row['distance']/row['speedlimit']

            

             if row['destination'] == curr_city:
                 source = cityGps[cityGps['city'] == row['destination']]
                 destination = cityGps[cityGps['city'] == row['source']]
                 cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                 heapq.heappush(fringe,[t_road + t_trip + (cost/1000),row['source'],segments, total_miles + row['distance'], total_hours + (row['distance']/row['speedlimit']) , t_road + t_trip ,path +" "+ row['source']])
   
             else:
                source = cityGps[cityGps['city'] == curr_city]
                destination = cityGps[cityGps['city'] == row['destination']]
                cost = haversine_distance(source['latitude'], source['longitude'],destination['latitude'],destination['longitude'])
                heapq.heappush(fringe,[t_road + t_trip + (cost/1000),row['destination'],segments, total_miles + row['distance'], total_hours + (row['distance']/row['speedlimit']) , t_road + t_trip,path+ " "+ row['destination']])


    routes= path.split(" ")

    route_taken = routes_structure(routes,roadSegments)

    return {"total-segments" : segments, 
            "total-miles" : float(total_miles), 
            "total-hours" : float(total_hours), 
            "total-delivery-hours" : float(total_delivery_hours), 
            "route-taken" : route_taken }


def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    cityGps = pd.read_csv('city-gps.txt', names=['city','latitude','longitude'] ,delim_whitespace=True)
    roadSegments = pd.read_csv('road-segments.txt', names=['source','destination','distance','speedlimit', 'name_of_highway'] ,delim_whitespace=True)
    cityGps=cityGps.drop_duplicates()

    maxspeed = max(roadSegments['speedlimit'])

    if cost == "segments":
        return optimum_segments(start,end,roadSegments,cityGps)
    elif cost == "distance":
        return optimum_distance(start,end,roadSegments,cityGps)
    elif cost == "time":
        return optimum_time(start,end,roadSegments,cityGps,maxspeed)
    elif cost == "delivery":
        return optimum_delivery_time(start,end,roadSegments,cityGps,maxspeed)






#ref https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine_distance( lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 

    if len(lon2) == 0 and len(lat2) == 0:
        return 0

    if len(lat1) == 0 and len(lon1) == 0:
        return 0

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])