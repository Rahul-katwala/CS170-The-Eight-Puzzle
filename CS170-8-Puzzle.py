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
    print_puzzle(puzzle)
    print('puzzle\n')
    return (str(h) + ' is the h cost \n')
    
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

                
if __name__ == "__main__":
    main()
