import copy
import time
import sys


def main():
    # Getting user input for if they want to use default or their own custom one
    inputnum = int(input("Welcome to an 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own.\n"))

    # Setting up the puzzle if user wants to create a custom puzzle
    if inputnum == 1:
        puzzle = ([0, 1, 2], [4, 5, 3], [7, 8, 6])
        
    else:
        print('Enter your puzzle, use a zero to represent the blank \n')

        # Gets the puzzle
        puzzle_row_one = raw_input('Enter the first row with spaces between each number: ').split(' ')
        puzzle_row_two = raw_input('Enter the second row with spaces between each number: ').split(' ')
        puzzle_row_three = raw_input('Enter the third row. with commas between each number: ').split(' ')
        # Changing all values to int
        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])
        puzzle = puzzle_row_one, puzzle_row_two, puzzle_row_three
        
    # Chooses heuristic and algorithm
    algorithmChoice = select_and_init_algorithm(puzzle)
    # Calling the search 
    print(uniform_cost_search(puzzle, algorithmChoice[0], algorithmChoice[1]))
    
    
#Chooses the algorithm
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
                    found += 1
                    if found == 2:
                        break
                if final_result[i][j] == l:
                    solution_row = i
                    solution_column = j
                    found += 1
                    if found == 2:
                        break
        #Add the sum of the two differences between the rows and columns             
        sum = sum + (abs(solution_row - current_row) + abs(solution_column - current_column))

    return sum
    
        
def misplaced(puzzle, puzzleLength):
    final_result = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    misplacedCounter = 0
    #returns the count of misplaced numbers when compared to the solution
    for row in range(puzzleLength):
        for column in range(puzzleLength):
            if int(puzzle[row][column]) != final_result[row][column]:
                if int(puzzle[row][column]) != 0:
                    # If they dont match and it is not a 0 then increment misplacedCounter by 1
                    misplacedCounter += 1
    return misplacedCounter
    
    
def uniform_cost_search(puzzle, h, algorithm):

    # Starts the time the algorithm started
    initialTime = time.time()
    # Initalizing the first node
    initialNode = node(puzzle)
    initialNode.hcost = h
    initialNode.depth = 0
    # We will use queue to hold all the nodes that were created but not explored yet
    queue = [initialNode]
    # encountered will be a hash of all the nodes puzzles we have already visited
    encountered = {str(initialNode.puzzle): '001'}
    nodeCount = -1
    queueSize = 1
    maxQueueSize = 0
    stack_to_print = []
    # We will stay in this while loop as long as the problem is not solved
    while True:
        
        if algorithm != "Uniform":
            # Using a lambda function to sort by lowest h(n) + g(n)
            # I got the resource for sorting from: https://docs.python.org/3/howto/sorting.html
            queue = sorted(queue, key=lambda x: (x.depth + x.hcost, x.depth))

        # set currentNode to the node top of the queue and increase the nodeCount by one 
        currentNode = queue[0]
        nodeCount += 1
        
        # If we solve the puzzle then print the traceback of the solution.
        if solved(currentNode.puzzle):
            # Gets full solution path in reverse 
            solutionPath = currentNode
            solutionPathList = []
            while solutionPath.parent != None:
                solutionPathList.append(solutionPath)
                solutionPath = solutionPath.parent
            
            for solutionPath in (stack_to_print):
                print_puzzle(solutionPath.puzzle)
                print('The best state to expand with a g(n) = ' + str(solutionPath.depth) + ' and h(n) = ' + str(solutionPath.hcost) + ' is?\n')
            
            print_puzzle(currentNode.puzzle)
            print('The best state to expand with a g(n) = ' + str(currentNode.depth) + ' and h(n) = ' + str(currentNode.hcost) + ' is?\n')
            # I got the resource for round from https://docs.python.org/3/library/functions.html?highlight=round#round
            print('Puzzle completed! \nThe number of nodes expanded were: ' + str(nodeCount) + '\nThe depth of the solution was: ' + str(currentNode.depth) + '\nThe max queue size is: ' + str(maxQueueSize) + '\nThe puzzle took ' + str(round((time.time()-initialTime), 1))  + ' seconds')
            # Gives chance to see the full solution path 
            inputnum = raw_input('Press 1 to see the solution path. Press anything else to quit\n')
            if inputnum == '1':
                print_puzzle(initialNode.puzzle)
                for solutionPath in reversed(solutionPathList):
                    print_puzzle(solutionPath.puzzle)
                return 'Ending...'
            else:
                return 'Ending...'
            
        # Expand all possible states from the node and place them into the child of the current node
        expanded_child_nodes = expand(currentNode, encountered)
        
        # Fill arr with the list of children nodes 
        childNodeList = [expanded_child_nodes.child1, expanded_child_nodes.child2, expanded_child_nodes.child3, expanded_child_nodes.child4]
        
        # pop the first element of queue since we have already encountered it
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
                #Add new node to queue and list of nodes we have encountered to make sure we do not see it again
                queue.append(newNode)
                queueSize += 1
                encountered[str(newNode.puzzle)] = '001'
        stack_to_print.append(currentNode)
        # Set maxQueueSize to the max of maxQueueSize and queueSize
        maxQueueSize = max(maxQueueSize, queueSize)
    
    
# Prints the puzzle
def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])

    print('\n')
    
    
#This function will return all the possible child nodes of currentNode
def expand(currentNode, encountered):
    current_row = 0
    current_column = 0

    # First find the position of the 0 on the current puzzle
    for i in range(len(currentNode.puzzle)):
        for j in range(len(currentNode.puzzle)):
            if int(currentNode.puzzle[i][j]) == 0:
                current_row = i
                current_column = j
                
    # Check to see if current_column is the first column. If it is not we can move left.
    if current_column != 0:
        #getChild will return the puzzle of the possible outcome after moving 0 to the appropriate location
        move_left = getChild(currentNode.puzzle, current_row, current_column, "left")
        
        # If this node already has been encountered, then we do not need to recounter it.
        if encountered.get(str(move_left)) == None:
            currentNode.child1 = node(move_left)

    # Check to see if current_column is the last column. If it is not we can move right.
    if current_column != len(currentNode.puzzle) - 1:
       
        move_right= getChild(currentNode.puzzle, current_row, current_column, "right")
    
        if encountered.get(str(move_right)) == None:
            currentNode.child2 = node(move_right)

    # Check to see if current_row is the first row. If it is not we can move up.
    if current_row != 0:
        
        move_up = getChild(currentNode.puzzle, current_row, current_column, "up")
        
        if encountered.get(str(move_up)) == None:
            currentNode.child3 = node(move_up)

    # Check to see if current_row is the last row. If it is not we can move down.
    if current_row != len(currentNode.puzzle) - 1:
       
        move_down = getChild(currentNode.puzzle, current_row, current_column, "down")
        
        if encountered.get(str(move_down)) == None:
            currentNode.child4 = node(move_down)

    
    return currentNode


def getChild(puzzle, current_row, current_column, direction):
# Resource used for deepcopy: https://docs.python.org/3/library/copy.html
    newNode = copy.deepcopy(puzzle)
    
    if (direction == "up"): # Swaps the 0 with the one which is one spot up
        # Swaps the tile and blank spot 
        temp = newNode[current_row - 1][current_column]
        newNode[current_row - 1][current_column] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    elif (direction == "down"): # Swaps the 0 with the one which is one spot down
        temp = newNode[current_row + 1][current_column]
        newNode[current_row + 1][current_column] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
        
    elif (direction == "right"): # Swaps the 0 with the one which is one spot right
        temp = newNode[current_row][current_column + 1]
        newNode[current_row][current_column + 1] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    elif (direction == "left"): # Swaps the 0 with the one which is one spot left
        temp = newNode[current_row][current_column - 1]
        newNode[current_row][current_column - 1] = newNode[current_row][current_column]
        newNode[current_row][current_column] = temp
    
    return newNode


# Checks if the puzzle has been solved
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
    

                
if __name__ == "__main__":
    main()
