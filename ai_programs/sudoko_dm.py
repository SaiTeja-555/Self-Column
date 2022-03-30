from logic import *

grid = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]


def sudoko():
    symbols = []
    for n in range(1,10):
        arr = []
        for i in range(len(grid)):
            row = []
            for j in range(len(grid[0])):
               row.append(Symbol(f"{i}_{j}_{n}"))
            arr.append(row)
        symbols.append(arr)

    knowledge = And()
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                knowledge.add(symbols[grid[i][j]-1][i][j])
    for arr in symbols:
        for i in range(len(grid)):
            knowledge.add(Or(*arr[i]))
            knowledge.add(Or(*[arr[j][i] for j in range(9)]))
        for x in range(3):
            for y in range(3):
                knowledge.add(Or(*[arr[i][j] for i in range(3*x,3*x+3) for j in range(3*y,3*y+3)]))

    for i in range(len(grid)):
        for j in range(len(grid)):
            for arr in symbols:
                knowledge.add(Implication(arr[i][j],Not(Or(*[arr2[i][j] for arr2 in symbols if arr2!=arr]))))

    print(knowledge.formula())
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                for n in range(9):
                    if model_check(knowledge,symbols[n][i][j]):
                        print("T",i,j,n+1)
                        grid[i][j] = n+1
                        break
                    else:
                        print("F",i,j,n+1)
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j],end = " ")
        print()
    
sudoko()

