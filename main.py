import os, time
from colorama import init, Fore, Back, Style, ansi
import numpy as np
import random
from Point import Point

# value_maze = [
#     [1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1, 0, 1],
#     [1, 1, 0, 0, 0, 1, 1, 1]
# ]

value_maze = np.random.randint(2, size=(7, 30)).tolist()

maze = []

def init_maze():
    for i, row in enumerate(value_maze):
        new_row = []
        for j, column in enumerate(row):
            cur_point = Point(j, i, str(column))
            new_row.append(cur_point)
        maze.append(new_row)

def generate_random_valid_entry_end() -> tuple:
    entry_point = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
    while entry_point.value != "1":
        entry_point = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
        
    end_point = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
    while end_point.value != "1" or end_point == entry_point:
        end_point = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
        
    return (entry_point, end_point)

# ! IN DEVELOPMENT
def generate_further_entry_end() -> tuple:
    all_dir = [(0,1), (0,-1), (1,0), (-1,0)]
    
    start = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
    while start.value != "1":
        start = maze[random.randint(0,len(maze)-1)][random.randint(0,len(maze[0])-1)]
        
    farthest_dist = float("-INF")
    farthest_point_possible = None
    
    visited = [start]
    queue = [start]
    while len(queue) != 0:
        current_point = queue.pop()
        
        dist_x, dist_y = current_point - start
        if(dist_x + dist_y > farthest_dist and
           current_point != start):
            farthest_dist =dist_x + dist_y
            farthest_point_possible = current_point
        
        visited.append(current_point)
        for dir in all_dir:
            neighbor_x, neighbor_y = current_point + dir
            
            if(in_maze(neighbor_x, neighbor_y)):
                neighbor = maze[neighbor_y][neighbor_x]
                if((neighbor not in visited) and neighbor.value == "1"):
                    neighbor.prev = current_point
                    queue.append(neighbor)
                    
    return (start, farthest_point_possible)

def is_path_start_end(start, end) -> bool:
    visited = [start]
    queue = [start]
    all_dir = [(0,1), (0,-1), (1,0), (-1,0)]
    
    while len(queue) != 0:
        current_point = queue.pop()
        visited.append(current_point)
        for dir in all_dir:
            neighbor_x, neighbor_y = current_point + dir
            
            if(in_maze(neighbor_x, neighbor_y)):
                neighbor = maze[neighbor_y][neighbor_x]
                if((neighbor not in visited) and neighbor.value == "1"):
                    neighbor.prev = current_point
                    queue.append(neighbor)
                    if(neighbor == end):
                        return True
    return False
    
    

def generate_maze_valid_path_start_end(random=True) -> tuple:
    global value_maze, maze
    
    if random:
        while True:
            maze = []
            value_maze = np.random.randint(2, size=(7, 30)).tolist()
            init_maze()
            start, end = generate_random_valid_entry_end()
            if(is_path_start_end(start=start,end=end)):
                return (start, end)
    
    maze = []
    value_maze = np.random.randint(2, size=(7, 30)).tolist()
    init_maze()
    return generate_further_entry_end()    

def main(start_end):
    all_dir = [(0,1), (0,-1), (1,0), (-1,0)]
    dir_to_symbol = ["v", "^", ">", "<"]
    
    def print_maze():
        os.system("cls")
        for line in maze:
            for point in line:
                color = Style.RESET_ALL
                if(point.value == "X"):
                    color = Fore.RED
                if(point.value in ("S", "E")):
                    color = Fore.GREEN
                if(point.value in dir_to_symbol):
                    color = Fore.YELLOW
                print(color + point.value, end=" ")
            print()
            
    entry_point, end_point = start_end
    
    visited = [entry_point]
    queue = [entry_point]

    found = False

    while len(queue) != 0 and not found:
        current_point = queue.pop()
        cur_original_val = current_point.value
        
        visit_original_value = [val.value for val in visited]
        for visit_node in visited:
            if(visit_node != entry_point):
                visit_node.value = dir_to_symbol[all_dir.index((visit_node.prev-visit_node))]
            
        current_point.value = "X"
        entry_point.value = "S"
        end_point.value = "E"
        
        print_maze()
        print(current_point)
        
        for visit_node, origin_val in zip(visited, visit_original_value):
            visit_node.value = origin_val
        
        current_point.value = cur_original_val
        entry_point.value = "1"
        end_point.value = "1"
        
        visited.append(current_point)
        for dir in all_dir:
            neighbor_x, neighbor_y = current_point + dir
            
            if(in_maze(neighbor_x, neighbor_y)):
                neighbor = maze[neighbor_y][neighbor_x]
                if((neighbor not in visited) and neighbor.value == "1"):
                    neighbor.prev = current_point
                    queue.append(neighbor)
                    if(neighbor == end_point):
                        found = True
                        break
        if(found):
            break
        time.sleep(0.5)
        
    if(found):
        prev_p = end_point.prev
        while prev_p != None:
            if(prev_p.prev != None):
                prev_p.value = dir_to_symbol[all_dir.index((prev_p.prev-prev_p))]
            prev_p = prev_p.prev
        
        end_point.value = "E"
        entry_point.value = "S"
        print_maze()
        print("FOUND")
    else:
        print("NOT FOUND")

def in_maze(x, y):
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze)

if __name__ == "__main__":
    init()
    main(generate_maze_valid_path_start_end(random=False))
    print(Style.RESET_ALL + "Finished")
    
    
    
    
    