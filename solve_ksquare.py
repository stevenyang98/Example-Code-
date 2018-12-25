def is_solved(config):
    "Return whether input config is solved"
    k = len(config)
    y=0
    for row in config:
        x=0# initialize at column zero
        for i in range(len(row)):
            calc_y=(row[i]-1)//k
            calc_x=row[i]-k*calc_y-1
            if calc_y == y:
                if x == calc_x:
                    x+=1#we move columns each iteration thru a row
                else:
                    return False
            else:
                return False
        y+=1 #moving on each row
    return True

def move(config, mv):
    "Return a new configuration made by moving config by move mv"
    k = len(config)
    (s, i) = mv         # s in ("row", "col") and i in range(k)
    #s designates which columns or row and i in the index in that column or row
    #program works for a single move


    #make into list first
    config_list=[]
    for row in config:
        row_list=[]
        for i in row:
            row_list.append(i)
        config_list.append(row_list)

    if mv[0] == "row":#if we are doing a row move
        row_number = mv[1]
        config_list[row_number] = config_list[row_number][::-1] #update the config to be in reverse now

        config_list[row_number]=[-1*i for i in config_list[row_number]]
    if mv[0] == "col":#if we are doing a column move
        top = 0
        bottom = -1 #pointers for column
        for step in range((k+1)//2):
            config_list[top][mv[1]], config_list[bottom][mv[1]] = -config_list[bottom][mv[1]], -config_list[top][mv[1]]
            top+=1
            bottom-=1
    return tuple([tuple(row) for row in config_list])

def solve_ksquare(config):
    "Return a list of moves that solves config"
    #we have path and path updater
    recorded=set()#empty set of what we have visited
    to_visit=[Path(config)]#first thing we visit is at Path instance of the configuration
    path=[]
    solved=False
    if is_solved(config):
        return path
    while not solved and to_visit:
        adj=neighbors(to_visit.pop(0)) #neighbors return adj list, feed in first configuration
        for i in adj:
            if i.config not in recorded:
                recorded.add(i.config)
                to_visit.append(i)
                if is_solved(i.config):
                    path = i.path
                    solved=True

    return path

class Path:
    #we need this class to store the path
    #when we find a new path add the parent's path
    #configuration gives us the next state
    def __init__(self, config, path=None):
        #every time we init a node object, we take the node as a configuration and it has no path at the moment
        if path is None:
            self.path=[] #make the path an empty list
        else:
            #if there is a path, update path to node
            self.path=path
        self.config=config #save the configuration #configuration of node

def neighbors(path): #spits out neigbhors
    neighbors=[]
    config=path.config
    for place in ["row","col"]: #add 2k moves
        for num in range(len(config)): #2k work
            neighbors.append(Path(move(config,(place,num)),path.path + [(place,num)]))#add move that results from it
    return neighbors