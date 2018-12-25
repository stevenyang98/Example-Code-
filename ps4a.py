# Problem Set 4A
# Name: Steven Yang
# Collaborators:
# Time Spent: 0:40
# Late Days Used: x

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree1 = [[4,10],5] # TODO: change this assignment
tree2 = [[15,4],[[1,2],10]] # TODO: change this assignment
tree3 = [[12],[14,6,2],[19]] # TODO: change this assignment


# Part A1: Multiplication on tree leaves

def mul_tree(tree):
    """
    Recursively computes the product of all tree leaves.
    Returns an integer representing the product.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
    Outputs
       total: An int equal to the product of all leaves of the tree.

    """

    # TODO: Your code here
    if tree == []: #base case
        return 1
    if type(tree) == int: #base case
        return tree
    else:
        return mul_tree(tree[0])*mul_tree(tree[1:]) #gradually go from high to low 


# Part A2: Arbitrary operations on tree leaves

def addem(a,b):
    """
    Example operator function.
    Takes in two integers, returns their sum.
    """
    return a + b

def prod(a,b):
    """
    Example operator function.
    Takes in two integers, returns their product.
    """
    return a * b

def op_tree(tree, op, base_case):
    """
    Recursively runs a given operation on tree leaves.
    Return type depends on the specific operation.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
       op: A function that takes in two inputs and returns the
       result of a specific operation on them.
       base_case: What the operation should return as a result
       in the base case (i.e. when the tree is empty).
    """

    if tree == []: #base
        return base_case
    elif type(tree) == int: #base
        return tree
    else: #using the op to plug in the op specified in the input
        return op(op_tree(tree[0], op, base_case), op_tree(tree[1:], op, base_case)) #reursively call op_tree in itself
    
    
    
    

# Part A3: Searching a tree

def search_odd(a, b):
    """
    Operator function that searches for odd values within its inputs.

    Inputs
        a, b: integers or booleans
    Outputs
        True if either input is equal to True or odd, and False otherwise
    """
    #Run conditions to see if a or b is either bool or int then have more conditionals for returns
    if (type(a) == bool or type(a) == int and a is not None) or (type(b) == bool or type(b) == int and b is not None):
        if (a == True or b == True) or (a%2 != 0 or b%2 != 0):
            return True
        elif (a == False and b == False) or (a%2 == 0 and b%2 == 0):
            return False
    else:
        return False

if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # Do not erase the pass statement below.
    pass
