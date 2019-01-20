import numpy as np

def solve(constraints):
    """
    Implement me!!!!!!!
    This function takes in a set of constraints. The first dimension is the axis
    to which the constraints refer to. The second dimension is the list of constraints
    for some axis index pair. The third demsion is a single constraint of the form
    [i,j] which means a run of i js. For example, [4,1] would correspond to a block
    [1,1,1,1].

    The return value of this function should be a numpy array that satisfies all
    of the constraints.
    A puzzle will have the constraints of the following format:


    array([
        [list([[4, 1]]),
         list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[2, 1]]),
         list([[1, 1], [1, 1]])],
        [list([[2, 1]]),
         list([[1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[1, 1], [1, 1]]),
         list([[5, 1]])]
        ], dtype=object)

    And a corresponding solution may be:
    array([[0, 1, 1, 1, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 0, 1],
           [0, 0, 0, 1, 1],
           [0, 0, 1, 0, 1]])
    
    """
    rowCons = constraints[0] #row constraints
    colCons = constraints[1] #col constraints
    rowNum = int(len(rowCons)) #total number of rows
    colNum = int(len(colCons)) #total number of cols
    total = rowNum * colNum

    rowAlters = [combination(data,colNum) for data in rowCons] 
    colAlters = [combination(data,rowNum) for data in colCons]
    # print(rowAlters)
    # print(colAlters)

    #Initialize
    solution = []
    for i in range(rowNum):
        solution.append(['X'] * colNum)

    #traverse all the positions, only leave the combinations that 
    #fulfill both the row and column contraints
    traverse = 0
    while traverse < total:
        row_value = set()
        col_value = set()
        for elem in rowAlters[int(traverse/colNum)]:
            row_value.add(elem[traverse%colNum])
        for elem in colAlters[int(traverse%colNum)]:
            col_value.add(elem[int(traverse/colNum)])

        intersect = row_value.intersection(col_value)
        for elem in rowAlters[int(traverse/colNum)]:
            if elem[int(traverse%colNum)] not in intersect:
                rowAlters[int(traverse/colNum)].remove(elem)
        for elem in colAlters[int(traverse%colNum)]:
            if elem[int(traverse/colNum)] not in intersect:
                colAlters[int(traverse%colNum)].remove(elem)
        traverse +=1
        
    # print(rowAlters)
    # print(colAlters)
    
    counter = 0
    while counter < total:
        temp = counter
        
        for i in range(rowNum):
            if rowAlters[i] == "F":
                continue
            if len(rowAlters[i]) == 0:
                return []
            elif len(rowAlters[i]) == 1:
                for j in range(colNum):
                    if solution[i][j] == 'X':
                        solution[i][j] = '0' if rowAlters[i][0][j] == 'X' else rowAlters[i][0][j]
                        counter += 1
                        checkIllegal(colAlters[j], i, solution[i][j])
                    elif solution[i][j] != rowAlters[i][0][j] and rowAlters[i][0][j] != 'X':
                        return []
                rowAlters[i] = 'F'
            else:
                for j in range(colNum):
                    if solution[i][j] != 'X':
                        continue
                    mark = checkDecide(rowAlters[i], j)
                    if mark is not None:
                        solution[i][j] = mark
                        counter += 1
                        checkIllegal(colAlters[j], i, mark)

        for i in range(colNum):
            if colAlters[i] == "F":
                continue
            if len(colAlters[i]) == 0:
                return []
            elif len(colAlters[i]) == 1:
                for j in range(rowNum):
                    if solution[j][i] == 'X':
                        solution[j][i] = '0' if colAlters[i][0][j] == 'X' else colAlters[i][0][j]
                        counter += 1
                        checkIllegal(rowAlters[j], i, solution[j][i])
                    elif solution[j][i] != colAlters[i][0][j] and colAlters[i][0][j] != 'X':
                        return []
                colAlters[i] = 'F'
            else:
                for j in range(rowNum):
                    if solution[j][i] != 'X':
                        continue
                    mark = checkDecide(colAlters[i], j)
                    if mark is not None:
                        solution[j][i] = mark
                        counter += 1
                        checkIllegal(rowAlters[j], i, mark)

        if temp == counter:
            return []
   
    print(solution)
    return np.array([[int(ele) for ele in solution[i]] for i in range(len(solution))])
   
    

# Given a list of constraint in row or column, and the length of column or row, 
# return all the possible combinations of the graph in the form of 'X' as blank. 
def combination(constraint, length):
    data_block = []
    data_color = []
    for elem in constraint:
        data_block.append(elem[0])
        data_color.append(elem[1])

    count_blank = 0
    for i in range(len(data_block)-1):
        if data_color[i] == data_color[i+1]:
            count_blank+=1

    datasum = sum(data_block)

    if len(constraint) == 0:
        return ['X' * length]

    j = 0
    result = []
    if len(constraint) == 1:
        j = 1

    for i in range(length - count_blank - datasum + 1):
        if j:
            header = 'X' * i + str(data_color[0]) * data_block[0]
            tails = ['X' * (length - len(header))]
        else:
            if data_color[0] == data_color[1]:
                header = 'X' * i + str(data_color[0]) * data_block[0] + 'X' * (1 - j)
            else:
                header = 'X' * i + str(data_color[0]) * data_block[0]
            tails = combination(constraint[1:], (length - len(header)))
        result.extend([header + tail for tail in tails])
    return result


#check if a cell fulfills the constraints 
def checkIllegal(alterset, idx, mark):
    if alterset != 'F' and len(alterset) > 1:
        tmark = mark if mark != '0' else 'X'
        for i in range(len(alterset) - 1, -1, -1):
            if alterset[i][idx] != tmark:
                alterset.pop(i)


#check if we can decide the combination
def checkDecide(alterset, idx):
    mark = alterset[0][idx]
    for j in range(1, len(alterset)):
        if mark != alterset[j][idx]:
            return None
    return '0' if mark == 'X' else mark



