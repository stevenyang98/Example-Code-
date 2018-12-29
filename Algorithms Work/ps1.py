###########################
# 6.0002
# Problem Set 1
# Name: Steven Yang
# Collaborators: Clay Jones 
# Time: 5.5 hours
#


from ps1_partition import get_partitions
import time
import copy

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file. Assumes the file contents contain data
    in the form of comma-separated values with the weight and cow name per line.

    Parameters:
    filename _ the name of the data file as a string

    Returns:
    a dictionary containing cow names (string) as keys, and the corresponding
    weight (int) as the value, e.g. {'Matt': 3, 'Kaitlin': 3, 'Katy': 5}
    """
    with open(filename,'r') as File_open:
        data = File_open.read().replace('\n','') # remove new lines in string format
    names = ''.join([i for i in data if not i.isdigit()]).strip(',') #removes starting comma
    keys = names.split(',')
    values = [int(i) for i in ''.join([i for i in data if i.isdigit()])]#get values by testing if is an instance of digit 
                                                                        #make i into int
    dictionary = dict(zip(keys,values))
    return dictionary


# Problem 2
def greedy_cow_trips(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows _ a dictionary of names (string), weights (int)
    limit _ weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    keys = sorted(cows, key=cows.get, reverse=True) #sort keys by the highest value
    big_trips = [] #big trips with the sublists
    copy_keys = keys[:] #shallow copy
    copy_cows = cows.copy()
    while len(keys) != 0: #it should equal zero at some point
        current_limit = 0 
        trips = []
#        import ipdb; ipdb.set_trace()
        for i in keys:
            if current_limit + copy_cows[i] <= limit: #standard greedy algorithm 
                trips.append(i)
                current_limit+=copy_cows[i]
                copy_keys.remove(i)
        keys = copy_keys[:] #make shallow copy as to avoid aliasing
        big_trips.append(trips) #adding the sublists to the biglist
    return big_trips
            

# Problem 3
def brute_force_cow_trips(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips.
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation.

    Does not mutate the given dictionary of cows.

    Parameters:
    cows _ a dictionary of names (string), and weights (int)
    limit _ weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    powerset = sorted(get_partitions(cows), key = len) #all possibilities according to length
    copy_cows = cows.copy() #avoid mutating original list
    result = []
    for sublists in powerset:
        viable = True #boolean flag to keep track of viable paths
        for items in sublists:
            weight = 0 #can start adding weights once I get to this point
            for names in items: #triple iteration to get to point where I can do dictionary lookup
                weight+=copy_cows[names]
            if limit <= weight:
                viable = False #taking note of which paths are viable 
                break
        if viable == True: #for those that do not go over weight limit
            if len(sublists)<len(result) or len(result) == 0: #storing and seeing which one is fewest trips
                result = sublists
    return result

# Problem 4
def compare_cow_trips_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_trips and brute_force_cow_trips functions here. Use the
    default weight limits of 10 for both greedy_cow_trips and
    brute_force_cow_trips.

    Print out the number of trips returned by each method and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    limit = 10
    greedy_start = time.time()
    greedy_cow_trips(cows, limit)
    greedy_end = time.time()
    print("Greedy time: " + str(greedy_end - greedy_start))
    brute_start = time.time()
    brute_force_cow_trips(cows, limit)
    brute_end = time.time()
    print("Brute force time: " + str(brute_end - brute_start))

# Problem 5
def dp_max_cows_on_trip(cow_weights, target_weight, memo = {}):
    """
    Find largest number of cows that can be brought back. Assumes there is
    an infinite supply of cows of each weight in cow_weights.

    Parameters:
    cow_weights   _ tuple of ints, available cow weights sorted from smallest to
                    largest value (d1 < d2 < ... < dk)
    target_weight _ int, amount of weight the spaceship can carry
    memo          _ dictionary, OPTIONAL parameter for memoization (you may not
                    need to use this parameter depending on your implementation,
                    don't delete though!)

    Returns:
    int, largest number of cows that can be brought back whose weight
    equals target_weight
    None, if no combinations of weights equal target_weight
    """
    if target_weight in memo:
        result = memo[target_weight] #if it's in it, do the dictionary lookup
    elif target_weight == 0: #base case
        return 0
    elif target_weight < 0: #control if not viable
        return None
    else:
        viable = [] #possible combinations
        for weights in cow_weights:
            result = dp_max_cows_on_trip(cow_weights, target_weight - weights, memo) #recursive call, what changes is the weight
            if result != None: #control for negative weight
                best_num = 1 + result #number of branches
                viable.append(best_num) #viable will have many things
        if len(viable) > 0: #not empty
            optimal = max(viable) #looking for maximum 
            memo[target_weight] = optimal #update the memo
        else:
            memo[target_weight] = None #control for none
    return memo[target_weight] 

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':

# Problem 1
    #cow_weights = load_cows('ps1_cow_data.txt')
    #print(cow_weights)
# Problem 2
    # print(greedy_cow_trips(cow_weights))
# Problem 3
    # print(brute_force_cow_trips(cow_weights))
# Problem 4
#     compare_cow_trips_algorithms()
# Problem 5
    # cow_weights = (3, 5, 8, 9)
    # n = 64
    # print("Cow weights = (3, 5, 8, 9)")
    # print("n = 64")
    # print("Expected ouput: 20 (3 * 18 + 2 * 5 = 64)")
    # print("Actual output:", dp_max_cows_on_trip(cow_weights, n))
    # print()
    pass
