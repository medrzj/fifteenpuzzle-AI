# Fifteen Puzzle 
# by Jessica Medrzycki 
# October 20, 2019
# Purpose:  15 puzzle solving algorithm, using 6 different search methods
#           Reports statistics when a solution is found
#
#                       To run this file:
#   python 15puzzle.py "123456789ABC DEF" <algorithm> <optional_heuristic_or_int_depth>
#
# Usage:    Program accepts command line arguments in format:
#           "[initialstate]" [algorithm] [options]
#               - initialstate must contain all characters:
#                   "123456789ABCDEF " in any order
#               - algorithm can be any of the following:
#                   BFS, DFS, DLS, ID, GBFS, A*
#               - options can be any of the following:
#                   int value for DLS
#                   'h1' or 'h2' for GBFS or AStar
# Output:   Prints statistics when solution found in format:
#               [depth], [numCreated], [numExpanded], [maxFringe]
#           Prints "-1, 0, 0, 0" if solution cannot be found


import sys
from copy import deepcopy

#our two potential solutions
#using list(board) converts user given string to this format
goal1 = ['1', '2', '3', '4', 
        '5', '6', '7', '8', 
        '9', 'A', 'B', 'C', 
        'D', 'E', 'F', ' ']

goal2 = ['1', '2', '3', '4', 
        '5', '6', '7', '8', 
        '9', 'A', 'B', 'C', 
        'D', 'F', 'E', ' ']

# Statistics objects
class Stats:
    depth = 0
    numCreated = 0
    numExpanded = 0
    maxFringe = 0

# Board object with depth and index of the piece 
class Board:
    depth = None
    board = []
    spaceIndex = None

    def __init__(self, givenBoard):
        self.depth = 0
        self.board = list(givenBoard)
        self.spaceIndex = self.board.index(' ')

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        return self.board == other.board

    def __repr__(self):
        return str(self)

    #compares a given goal list with Board.board
    def isGoalState(self, other):
        return self.board == other
        #return self.board[1:12] == other[1:12] and self.board[15] ==other[15]


def printStats(stats):
    print(str(stats.depth) + ', ' + str(stats.numCreated) + ', ' + str(stats.numExpanded) + ', ' + str(stats.maxFringe))

#returns a list of all the potential moves the blank space can make
def potentialMoves(board):
    #given order to expand the graph
    expandOrder = ['R', 'D', 'L', 'U']
    rIndex = [3,7,11,15] #cannot move right in index 3,7,11,15
    dIndex = [12,13,14,15] #cannot move down in index 12,13,14,15
    lIndex = [0,4,9,12] #cannot move left in index 0,4,8,12
    uIndex = [0,1,2,3] #cannot move up in index 0,1,2,3

    fringe = [] #list of expanded nodes
    
    for move in expandOrder:
        if move == 'R' and board.spaceIndex not in rIndex: 
            nextState = deepcopy(board)
            nextMoveIndex = nextState.spaceIndex + 1 
            fringe.append(__updateBoard(nextState, nextMoveIndex))

        if move == 'D' and board.spaceIndex not in dIndex: 
            nextState = deepcopy(board)
            nextMoveIndex = nextState.spaceIndex + 4 
            fringe.append(__updateBoard(nextState, nextMoveIndex))

        if move == 'L' and board.spaceIndex not in lIndex: 
            nextState = deepcopy(board)
            nextMoveIndex = nextState.spaceIndex -1
            fringe.append(__updateBoard(nextState, nextMoveIndex))

        if move == 'U' and board.spaceIndex not in uIndex: 
            nextState = deepcopy(board)
            nextMoveIndex = nextState.spaceIndex - 4
            fringe.append(__updateBoard(nextState, nextMoveIndex))

    return fringe


def __updateBoard(nextState, nextMoveIndex):
    nextState.depth += 1
    #move new piece into blank spot
    nextState.board[nextState.spaceIndex] = nextState.board[nextMoveIndex] 
    nextState.board[nextMoveIndex] = ' '
    nextState.spaceIndex = nextMoveIndex
    return nextState

def heuristic_Manhattan(board):
    manDistance = 0
    state = board.board
    for tile in state:
        index = state.index(tile)
        solution = goal1.index(tile)
        if index != solution:
            manDistance += abs(solution/4 - index/4) + abs(solution%4 -  index%4)
    return manDistance

def heuristic_Misplaced(board):
    sum = 0
    state = board.board
    for tile in state:
        index = state.index(tile)
        solution = goal1.index(tile)
        if index != solution:
            sum += 1
    return sum

def BFSalgorithm(stats, board):
    #BFS uses queue (FIFO)
    queue = [board]
    path = []
    while(queue):
        currentState = queue.pop(0)
        #is it the solution? 
        if currentState.isGoalState(goal1) or currentState.isGoalState(goal2):
            stats.depth = currentState.depth
            printStats(stats)
            sys.exit(-1)
        else:
            #is not, so go to each board
            adjMoves = potentialMoves(currentState)
            #state is visited
            path.append(currentState)
            stats.numExpanded += 1
            for state in adjMoves:
                if state not in path: #if next node not already visited
                    queue.append(state)
                    stats.numCreated += 1
                    if len(queue) > stats.maxFringe:
                        stats.maxFringe = len(queue)

    print(printStats(stats) + " NO SOLUTION")
    for state in path:
         print(state)

def DFSalgorithm(stats, board):
    stack = [board]
    path = []

    while(stack):
        currentState = stack.pop()  #LIFO
        if currentState.isGoalState(goal1) or currentState.isGoalState(goal2):
            stats.depth = currentState.depth
            printStats(stats)
            sys.exit(-1)
        else:
            #is not, so go to each board
            adjMoves = potentialMoves(currentState)
            #state is visited
            path.append(currentState)
            stats.numExpanded += 1
            for state in adjMoves:
                if state not in path: 
                    stack.append(state)
                    stats.numCreated += 1
                    if len(stack) > stats.maxFringe:
                        stats.maxFringe = len(stack)

    printStats(stats)

def DLSalgorithm(stats, board, maxiteration):
    stack = [board]
    path = []

    while(stack):
        currentState = stack.pop()  #LIFO
        if currentState.isGoalState(goal1) or currentState.isGoalState(goal2):
            stats.depth = currentState.depth
            printStats(stats)
            sys.exit(-1)
        else:
            #is not, so go to each board
            adjMoves = potentialMoves(currentState)
            #state is visited
            path.append(currentState)
            stats.numExpanded += 1
            for state in adjMoves:
                if state not in path: 
                    if state.depth <= maxiteration:
                        stack.append(state)
                        stats.numCreated += 1
                        if len(stack) > stats.maxFringe:
                            stats.maxFringe = len(stack)

    printStats(stats)

def GBFSalgorithm(stats, board, h):
    #GBFS uses priority queue 
    if h == 'h1':
        heuristic = heuristic_Misplaced(board)
    else: heuristic = heuristic_Manhattan(board)
        
    queue = [board]
    heuristicPQ = [heuristic]
    path = []
    while(queue):
        currentState = queue.pop(0)
        heuristicPQ.pop(0)
        #is it the solution? 
        if currentState.isGoalState(goal1) or currentState.isGoalState(goal2):
            stats.depth = currentState.depth
            printStats(stats)
            sys.exit(-1)
        else:
            #is not, so go to each board
            adjMoves = potentialMoves(currentState)
            #state is visited
            path.append(currentState)
            stats.numExpanded += 1
            for state in adjMoves:
                if state not in path: #if next node not already visited
                    
                    if h == 'h1': heuristic = heuristic_Misplaced(state)
                    else: heuristic = heuristic_Manhattan(state)

                    [heuristicPQ, index] = insertByPriority(heuristicPQ, heuristic)
                    queue.insert(index,state)
                    stats.numCreated += 1
                    if len(queue) > stats.maxFringe:
                        stats.maxFringe = len(queue)

    printStats(stats)

def ASTARalgorithm(stats,board,h):
    #A* uses priority queue and queued by heuristic & depth of the board
    if h == 'h1': heuristic = heuristic_Misplaced(board)
    else: heuristic = heuristic_Manhattan(board)
        
    queue = [board]
    heuristicPQ = [heuristic]
    path = []
    while(queue):
        currentState = queue.pop(0)
        heuristicPQ.pop(0)
        #is it the solution? 
        if currentState.isGoalState(goal1) or currentState.isGoalState(goal2):
            stats.depth = currentState.depth
            printStats(stats)
            sys.exit(-1)
        else:
            #is not, so go to each board
            adjMoves = potentialMoves(currentState)
            #state is visited
            path.append(currentState)
            stats.numExpanded += 1
            for state in adjMoves:
                if h == 'h1': heuristic = heuristic_Misplaced(state)
                else: heuristic = heuristic_Manhattan(state)
                if state not in path: #if next node not already visited
                    [heuristicPQ, index] = insertByPriority(heuristicPQ, heuristic + state.depth)
                    queue.insert(index,state)
                    stats.numCreated += 1
                    if len(queue) > stats.maxFringe:
                        stats.maxFringe = len(queue)

                elif state.depth < path[path.index(state)].depth : 
                    #current state is better solution than node already visitied
                    path[index].depth = state.depth
                    [heuristicPQ, index] = insertByPriority(heuristicPQ, heuristic + state.depth)
                    queue.insert(index,state)

    printStats(stats)

     
#returns a list with the priority queue and the index of insertion
def insertByPriority(queue, h):
    pq = queue
    j = -1
    for item in pq:
        j += 1
        if h < item:
            pq.insert(j, h)
            return [pq, j]
    pq.append(h)
    return [pq, j]



if __name__ == "__main__":

    if len(sys.argv) >= 3:
        stats = Stats() #stats object
        board = Board(sys.argv[1]) #puzzle object to solve 
        algorithm = sys.argv[2]

        if len(sys.argv) is 4:
            if sys.argv[3] == 'h1' or sys.argv[3] == 'h2':
                heuristic = sys.argv[3] 
            else: 
                dlsIterations = int(sys.argv[3])
    else:
        print('invalid input! ')
        sys.exit(-1)

    if algorithm == 'BFS':
        BFSalgorithm(stats, board)
    elif algorithm == 'DFS':
        DFSalgorithm(stats, board)
    elif algorithm == 'DLS':
        DLSalgorithm(stats, board, dlsIterations)
    elif algorithm == 'GBFS':
        GBFSalgorithm(stats, board, heuristic)
    elif algorithm == 'A*':
        ASTARalgorithm(stats, board, heuristic)



