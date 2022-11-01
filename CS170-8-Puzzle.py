import copy
import time
import sys


def main():
    
    # Ask user if they want to use a default puzzle or make their own
    inputnum = int(input("Welcome to an 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own.\n"))

    # If user wants a default puzzle
    if inputnum == 1:
        puzzle = ([0, 1, 2], [4, 5, 3], [7, 8, 6])
        
    else:
        print('Enter your puzzle, use a zero to represent the blank \n')

        # Gets first row
        puzzle_row_one = raw_input('Enter the first row with spaces between each number: ').split(' ')

        # Gets second row
        puzzle_row_two = raw_input('Enter the second row with spaces between each number: ').split(' ')

        # Gets third row
        puzzle_row_three = raw_input('Enter the third row. with commas between each number: ').split(' ')
        # Converts all elements in array to a type int
        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])
        puzzle = puzzle_row_one, puzzle_row_two, puzzle_row_three
        
    # Allowing the user to choose heuristic and algorithm
    algorithmChoice = select_and_init_algorithm(puzzle)
    # Running the program and printing the output
    print(uniform_cost_search(puzzle, algorithmChoice[0], algorithmChoice[1]))
    
    
def select_and_init_algorithm(puzzle):
    algorithm = int(input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, "
    "or (3) the Manhattan Distance Heuristic.\n"))
    h = 0
    if (algorithm == 3):
        h = manhattan(puzzle, 3)
        return h, "Manhattan"
    elif (algorithm == 2):
        h = misplaced(puzzle, 3)
        return h, "Misplaced"
    return h, "Uniform"
    
    
def manhattan(puzzle, puzzleLength):
    final_result = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    sum = 0
    solution_row = 0
    solution_column = 0
    current_row = 0
    current_column = 0
    found = 0
    #returns the sum of the distance of each number position and it's position on the solution path
    for l in range(1, 9):
        found = 0
        for i in range(puzzleLength):
            #if found == 2 then break out of loop as this number has been accounted for
            if found == 2:
                break
            for j in range(puzzleLength):
                if puzzle[i][j] == l:
                    current_row = i
                    current_column = j
                    found+=1
                    if found == 2:
                        break
                if final_result[i][j] == l:
                    solution_row = i
                    solution_column = j
                    found+=1
                    if found == 2:
                        break
        #Add the sum of the two differences between the rows and columns             
        sum = sum + (abs(solution_row-current_row) + abs(solution_column-current_column))

    return sum
    
        
def misplaced(puzzle, puzzleLength):
    final_result = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0
    #returns the count of misplaced numbers when compared to the solution
    for i in range(puzzleLength):
        for j in range(puzzleLength):
            if int(puzzle[i][j]) != final_result[i][j]:
                if int(puzzle[i][j]) != 0:
                    count += 1
    return count
    
def uniform_cost_search(puzzle, h, algorithm):


    initialTime = time.time()
    
    initialNode = node(puzzle)
    initialNode.hcost = h
    initialNode.depth = 0
    
    queue = [initialNode]
    encountered = [initialNode.puzzle]
    nodeCount = -1
    queueSize = 1
    maxQueueSize = 0
    print('The best state to expand with a g(n) = ' + str(initialNode.depth) + ' and h(n) = ' + str(initialNode.hcost) + ' is?\n')
    print_puzzle(initialNode.puzzle)
    stack_to_print = []
    # We will stay in this while loop as long as the problem is not solved
    while True:
        # Sort the queue for the lowest h(n) + g(n)
        if algorithm != "Uniform":
            # Using a lambda function to sort by lowest h(n) + g(n)
            # I got the resource for sorting from: https://docs.python.org/3/howto/sorting.html
            queue = sorted(queue, key=lambda x: (x.depth + x.hcost, x.depth))

        # set currentNode to the node top of the queue and increase the nodeCount by one 
        currentNode = queue[0]
        nodeCount += 1
        

        # If we get the solution puzzle then traceback and print all data
        if solved(currentNode.puzzle):
            
            
        currentNode.expanded = True
        expanded_child_nodes = expand(currentNode, encountered)
        
        # Fill arr with the list of children nodes 
        childNodeList = [expanded_child_nodes.child1, expanded_child_nodes.child2, expanded_child_nodes.child3, expanded_child_nodes.child4]
        
        
        queue.pop(0)
        queueSize -= 1
        # Updates the newNodes information 
        for newNode in childNodeList:
            if newNode is not None:
            # Calculate the newNodes h cost
                if algorithm == "Uniform":
                    newNode.hcost = 0
                elif algorithm == "Misplaced":
                    newNode.hcost = misplaced(newNode.puzzle, 3)
                elif algorithm == "Manhattan":
                    newNode.hcost = manhattan(newNode.puzzle, 3)
                # Updates the depth and parent for the newNodes
                newNode.depth = currentNode.depth + 1
                newNode.parent = currentNode
                #Add new node to queue and list of nodes we have encountered
                queue.append(newNode)
                queueSize += 1
                
                encountered.append(newNode.puzzle)
        stack_to_print.append(currentNode)
        # Set maxQueueSize to the max of maxQueueSize and queueSize
        maxQueueSize = max(maxQueueSize, queueSize)
    
# Prints the puzzle
def print_puzzle(puzzle):

    for i in range(0, 3):
        print(puzzle[i])

    print('\n')
    
#This function allows us to expand the node to other nodes that it could possibly become after moving 0.
def expand(currentNode, encountered):
    current_row = 0
    current_column = 0

  
    for i in range(len(currentNode.puzzle)):
        for j in range(len(currentNode.puzzle)):
            if int(currentNode.puzzle[i][j]) == 0:
                current_row = i
                current_column = j

    
 
    if current_column != 0:

        move_left = expand_swap(currentNode.puzzle, current_row, current_column, "left")
        
        if move_left not in encountered:
            currentNode.child1 = node(move_left)

    if current_column != len(currentNode.puzzle)-1:
       
        move_right= expand_swap(currentNode.puzzle, current_row, current_column, "right")
    
        if move_right not in encountered:
            currentNode.child2 = node(move_right)

    if current_row != 0:
        
        move_up = expand_swap(currentNode.puzzle, current_row, current_column, "up")
        
        if move_up not in encountered:
            currentNode.child3 = node(move_up)

    if current_row != len(currentNode.puzzle) - 1:
       
        move_down = expand_swap(currentNode.puzzle, current_row, current_column, "down")
        
        if move_down not in encountered:
            currentNode.child4 = node(move_down)

    
    return currentNode


def expand_swap(puzzle, current_row, current_column, direction):

    newNode = copy.deepcopy(puzzle)
    
    if (direction == "up"): # Swaps the 0 with the one which is one spot up
        temp = newNode[current_row-1][current_column]
        newNode[current_row-1][current_column] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    elif (direction == "down"): # Swaps the 0 with the one which is one spot down
        temp = newNode[current_row+1][current_column]
        newNode[current_row+1][current_column] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
        
    elif (direction == "right"): # Swaps the 0 with the one which is one spot right
        temp = newNode[current_row][current_column+1]
        newNode[current_row][current_column+1] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    elif (direction == "left"): # Swaps the 0 with the one which is one spot left
        temp = newNode[current_row][current_column-1]
        newNode[current_row][current_column-1] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    return newNode


def solved(puzzle):
    final_result = ([1, 2, 3], [4, 5, 6], [7, 8, 0])

    if puzzle == final_result:
        return True
    return False

class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hCost = 0
        self.depth = 0
        self.child1 = None
        self.child2 = None
        self.child3 = None
        self.child4 = None
        self.parent = None
        self.expanded = False
    

                
if __name__ == "__main__":
    main()
