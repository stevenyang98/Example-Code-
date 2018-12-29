def min_heapify(A,i):
    '''
    A: A list
    i: An int
    An array representing of min heap
    '''
   
    left_child=2*i+1 #left child
    right_child=2*i+2 #right child
    smallest=i
    if left_child < len(A) and A[left_child] < A[i]: #so if the child exists and if the child is greatest than the parent
        smallest=left_child
    if right_child < len(A) and A[right_child]< A[smallest]:
        smallest=right_child #getting ready for the swap
    if smallest!=i: #if the largest is not at index i
        A[i], A[smallest] = A[smallest],A[i] #swap left or right
        min_heapify(A,smallest) # recurse down the list comparing everything to new largest

def min_heapify_up(A,i):
    while i>0:
        if i>0 and A[i]<A[(i-1)//2]:
            A[i],A[(i-1)//2]=A[(i-1)//2],A[i]
        i = (i-1)//2

def extract_min(Q):
    Q[0], Q[len(Q) - 1] = Q[len(Q) - 1],Q[0]
    result = Q.pop()
    min_heapify(Q, 0)
    return result

def build_heap(A):
    '''
    :param A: list
    :return: a list representing a maximum heap
    '''
    for i in range(len(A)//2, -1, -1):
        min_heapify(A,i)
    return A


def insert_heap(A,l):
    '''
    A: heap
    l: int
    Return: Heap with element in it
    ''' 
#    A=list(A)
    A.append(l)
    min_heapify_up(A,len(A)-1)

def proximate_sort(A, k):
    ''' 
    Return an array containing the elements of 
    input tuple A appearing in sorted order.
    Input:  k | an integer < len(A)
            A | a k-proximate tuple
    '''
    A=list(A)
    to_return = []
    heap = build_heap(A[:k+1]) #make heap out of the first k elements of A
    remaining_A=A[k+1:] # this is the rest of k
    for i in remaining_A: #iterate thru the array we have made
        to_return.append(extract_min(heap))#always pop the first element in heap as a min heap that will be the minimum element
        #constant work
        insert_heap(heap, i)  # insert rest of elements into heap (logk) work
    for j in range(len(heap)): #last k elements
        #min_heapify(heap, 0) #
        to_return.append(extract_min(heap))
    return to_return
