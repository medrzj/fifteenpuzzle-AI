15 puzzle solving algorithm, using 6 different search methods and reports statistics when a solution is founnd

Program accepts command line arguments in format:
     "[initialstate]" [algorithm] [options]
        - initialstate must contain all characters:
                   "123456789ABCDEF " in any order
        - algorithm can be any of the following:
                    BFS, DFS, DLS, ID, GBFS, A*
        - options can be any of the following:
                    int value for DLS
         'h1' or 'h2' for GBFS or AStar



How to run 15puzzle.py:
	Example: 	python 15puzzle.py "6D7A89B F2C5E314" GBFS h2

For each of the search algorithms:
	BFS
	DFS
	GBFS	h1 
	A*	h2
	DLS	<num_depth>

GBFS and A* can take either h1 or h2 as their arguments for the heuristic
	- Ôh1Õ is the heuristic for the sum of tiles misplaced from the solution
	- Ôh2Õ is the manhattan distance 

DLS takes a number for the maximum depth to reach
	

Output for each algorithm:
cmd: 	python 15puzzle.py "123456789ABC DEF" BFS
      3, 19, 8, 12

cmd:	python 15puzzle.py "123456789ABC DEF" DFS
      1237, 2518, 1264, 1256

cmd: 	python 15puzzle.py "123456789ABC DEF" DLS 10
      3, 3302, 3302, 13

cmd: 	 python 15puzzle.py "123456789ABC DEF" GBFS h1
	13, 59, 27, 33

cmd: 	python 15puzzle.py "123456789ABC DEF" GBFS h2
	13, 525, 268, 258

cmd: 	python 15puzzle.py "123456789ABC DEF" A* h1
      13, 258, 122, 137

cmd: python 15puzzle.py "123456789ABC DEF" A* h2
      13, 230, 113, 118
      
Time complexity:
      BFS:	O(b^d) = max_branching^(depth) = 4^d
      DFS:	O(b^m) = max_branching^(max_depth)  =  4^d
      DLS:    O(b^d) = max_branching^(max_depth_limit) =  4^l
      GBFS   O(b^d) = max_branching^(max_depth) = 4^d
      A*	O(b^d) = max_branching^(max_depth) = 4^d
