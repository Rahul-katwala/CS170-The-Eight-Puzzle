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
        puzzle_row_one = input('Enter the first row with spaces between each number: ').split(' ')

        # Gets second row
        puzzle_row_two = input('Enter the second row with spaces between each number: ').split(' ')

        # Gets third row
        puzzle_row_three = input('Enter the third row. with commas between each number: ').split(' ')
        # Converts all elements in array to a type int
        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])
        puzzle = puzzle_row_one, puzzle_row_two, puzzle_row_three
        
    # Let user choose which algorithm they would like to use. Will return h value and string representing which algorithm as a tuplet
    algorithmChoice = select_and_init_algorithm(puzzle)
   

# function to choose the algorithm and calculate h
def select_and_init_algorithm(puzzle):
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, "
    "or (3) the Manhattan Distance Heuristic.\n")
    h = 0
    if (algorithm == 3):
        # h = manhattan(puzzle, puzzleLength)
        # return h, "Manhattan"
    elif (algorithm == 2):
        # h = misplaced(puzzle, puzzleLength)
        # return h, "Misplaced"
    return h, "Uniform"
    

    
# Prints the puzzle
def print_puzzle(puzzle):

    for i in range(0, 3):
        print(puzzle[i])

    print('\n')

                
if __name__ == "__main__":
    main()
