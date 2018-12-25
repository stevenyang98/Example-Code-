def squared_distance(p, q):
    '''Returns the squared distance between points p and q'''
    (px, py), (qx, qy) = p, q
    return (px - qx)**2 + (py - qy)**2

def closest_pair(points):
    ''' 
    Input:  points | tuple of at least 2 points of the form (x, y)
    Output: smallest squared distance between any pair of points
    '''
    shortest=0 #initialize what we are going to return
    points = sorted(points, key=lambda tup: tup[0]) #sort according to elt, which is the x-coordinate
    if len(points) == 2:
        return squared_distance(points[0],points[1])
    elif len(points) == 1: #stop if the list becomes odd
        return None
    else:
        length = len(points)
        middle_x = length//2
        left = closest_pair(points[:middle_x])
        right = closest_pair(points[middle_x:])
        x_median = points[middle_x][0]
        if left is None:
            left = right+1
        elif right is None:
            right = left+1 #this block ensures that a correct min is returned
        delta = min(left, right)
        within_delta = []
        for point in points: #iterate thru what we have so far
            if point[0] < delta+x_median and point[0] > x_median-delta: #if we are within width 2 delta
                within_delta.append(point)
        within_delta = sorted(within_delta, key=lambda elt: elt[1])#sort according to y values
        for possible in range(len(within_delta)): #iterate thru points sorted by y coordinate
            try:
                distance = squared_distance(within_delta[possible], within_delta[possible+1])
                if distance < delta:
                    delta=distance
            except IndexError:
                break
    return delta


