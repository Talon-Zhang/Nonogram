import numpy
from ./solve.py import *

constraints = [
		[
			[[4, 1]], 
			[[1, 1], [1, 1], [1, 1]],
        	[[3, 1], [1, 1]], 
			[[2, 1]], 
			[[1, 1], [1, 1]]
		],
        [
        	[[2, 1]], 
		 	[[1, 1], [1, 1]], 
		 	[[3, 1], [1, 1]],
         	[[1, 1], [1, 1]], 
		 	[[5, 1]]
		]
]


if __name__ == '__main__':
	print(solve(constraints))
	


	# And a corresponding solution may be:

	# array([[0, 1, 1, 1, 1],
	# 	   [1, 0, 1, 0, 1],
	# 	   [1, 1, 1, 0, 1],
	# 	   [0, 0, 0, 1, 1],
	# 	   [0, 0, 1, 0, 1]])