Abstraction:

1. Set of states S
2. Initial State S0 which is the source location.
3. A successor function which returns the nearest possible locations from the source location.
4. Goal state which is our destintion location.
5. A cost function that estimates how expensive a given set of moves is ( which we can get it from road-segment data)
6. A heuristic function that estimates how promising a given state is. Here cost is return based on segments, distance , time or delivery.


Approach:

Based on the given cost function given by the user, we call one of the functons,i.e., optimum_distance, optimum_segments, optimum_delivery_time, optimum_time. In these functions, we use fringe to store our states which has all the data required for that particular state. At first we would sort the fringe data using heapq and then pop the elements one by one based on the priority. The Priority is called based on the cost function which is passed. For example, to find the optimum distance to reach the destination, first we would fetch the data from road_segments file and filter the  data based on initial source, then from this point we would get all its nearest destnination. To make the next move, We have H(s) using the haversine formula to get the distance using the latitude and longitues and the priority will be set for that state and pushed into fringe data-structure. This process repeates untill we reach the destination. Once the destination is reached, we would come out of the loop by skipping the remaining steps as we would have already got the optimized solution.

Challenges:

1. For some location, there was no latitute and longitute values which caused error in the program and was also yielding wrong soltuion, when checked with 0 values for the same. Then through inscribe discussion, we got an idea to make H(s) as Zero for those cases.
2. One duplicate record was present in city-Gps.txt which caused issuing in many test cases and It took losts of time to find the root cause and finally duplicate was removed and error was fixed.
3. Writing priority for each cost functions was also a challenge as our calculated priority value was failing for few test cases intially.
4. Directly adding the haversine distance as an priority value was not yeidling the solution as it was masking the g(s) function value. So we had to reduce its value to get the required solution.
5. Reading Data using pandas and avoiding index was an issue 
