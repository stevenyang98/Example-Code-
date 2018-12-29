def search_sorted_2D_array(A, v):
    '''
    Return tuple (x, y) such that A[y][x] == v, or None.
    Input:  A | Array of equal length arrays of integers
              |     representing the rows of a 2D array
              |     where A[y][x] >= A[y - 1][x] and
              |           A[y][x] >= A[y][x - 1]
              |     for all (x, y) in range.
            v | An integer to search for in A.
    '''
    y=len(A)
    index_y=y-1
    x=0
    start=A[index_y][x] #start at left most corner
    tup = (x, y - 1)#place holder
    found=None
    while not found: #while loop
        try:
            if v == start: #best care scenario
                found=True
            elif v > start: #if it's greater
                x+=1
                start = A[index_y][x]  # move to the right one
                tup=(x,index_y)
            else: #if it's less
                index_y-=1
                start = A[index_y][x]  # move up one
                tup=(x,index_y)
        except IndexError: #if it's not in the thing, we handle this error by setting tup equal to none
            tup=None
            found=True
    return tup
