import argparse

class Node:
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.array = []

    def add(self,node):
        self.array.append(node)

    def is_empty(self):
        return len(self.array) == 0

    def contains_state(self,state):
        return any([state == node.state for node in self.array])

    def remove(self):
        if self.is_empty():
            raise Exception("Empty")
        return self.array.pop()

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.is_empty():
            raise Exception("Empty")
        return self.array.pop(0)

class SpecialFrontier(StackFrontier):
    def remove(self,cost_array):
        if self.is_empty():
            raise Exception("Empty")
        min_index = 0
        for i in range(len(self.array)):
            if cost_array[self.array[i].state[0]][self.array[i].state[1]] < cost_array[self.array[min_index].state[0]][self.array[min_index].state[1]]:
                min_index = i
        return self.array.pop(min_index)

def cost(state1,state2):
    return abs(state1[0]-state2[0])+abs(state1[1]-state2[1])
        

class Maze():
    def __init__(self,filename,opt):
        self.opt = opt
        with open(filename,'r') as f:
            contents = f.read()
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.intial_state = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        self.cost_array = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(cost((i,j),self.goal))
            self.cost_array.append(row)
        

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("#", end = "")
                elif (i,j) == self.intial_state:
                    print("A", end = "")
                elif (i,j) == self.goal:
                    print("B", end = "")
                elif solution is not None and (i,j) in solution:
                    print("*", end = "")
                elif (i,j) in self.explored_nodes:
                    print("-", end = "")
                else:
                    print(" ", end = "")
            print()
        print()
        print()
        print("Number of explored nodes = ",self.num_explored)

    def neighbours(self,state):
        row,col = state

        candidates = [
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))
            ]
        
        result = []
        for action,(r,c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action,(r,c)))
            except IndexError:
                continue
        return result
                    

    def solve(self):
        self.num_explored = 0
        start = Node(state = self.intial_state, parent = None, action = None)
        if self.opt == 1:
            frontier = StackFrontier()
        elif self.opt == 2:
            frontier = QueueFrontier()
        elif self.opt == 3:
            frontier = SpecialFrontier()
        frontier.add(start)
        self.explored_nodes = set()
        
        while True:
            #print("s")
            #print([node.state for node in frontier.array])
            self.print()
            if frontier.is_empty():
                raise Exception("no solution")
            if self.opt == 3:
                node = frontier.remove(self.cost_array)
            else:
                node = frontier.remove()
            self.num_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            self.explored_nodes.add(node.state)
            #print(self.neighbours(node.state))
            for action,state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored_nodes:
                    child = Node(state = state, parent = node, action = action)
                    frontier.add(child)
            
            
parser = argparse.ArgumentParser(description = "Maze solving")
parser.add_argument('-f','--filename',type=str,required = True, help="filename of the maze")
args = parser.parse_args()

if __name__ == "__main__":
    
    maze = Maze(args.filename,3)
    maze.solve()
    maze.print()
