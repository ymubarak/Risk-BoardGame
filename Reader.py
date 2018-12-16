from Territory import *
from Continent import *

def read_game(file_path):
    continents = []
    graph = {}
    file = open(file_path, "r")
    try:
        line = next(file).strip()
        v = int(line.split(" ")[-1])
        
        # create graph map
        for i in range(1, v+1):
            graph[i] = Territory(i)
        
        # read edges
        line = next(file).strip()
        e = int(line.split(" ")[-1])
        for i in range(e):
            line = next(file)[1:-2] # skip parenthesis
            edge_pair = line.split(" ")
            t_from = int(edge_pair[0])
            t_to = int(edge_pair[1])
            graph[t_from].add_neighbor(graph[t_to])
            graph[t_to].add_neighbor(graph[t_from])
        
        # read continents
        line = next(file).strip()
        p = int(line.split(" ")[-1])
        for i in range(p):
            arr = next(file).strip().split(" ")
            bonus = int(arr[0])
            territories = []
            for t_id in arr[1:]:
                territories.append(graph[int(t_id)])
            
            c = Continent(bonus, territories)
            continents.append(c)

        t1 = []
        t2 = []
        for i in range(v):
            line = next(file).strip()
            detail = line.split(" ")
            t_id = int(detail[0])
            p_num = int(detail[1])
            n_arm = int(detail[2])
            if p_num == 1:
                t1.append(graph[t_id])
            elif p_num == 2:
                t2.append(graph[t_id])
            graph[t_id].n_armies = n_arm


    except StopIteration:
        pass
    except FileNotFoundError:
        print("Error, File not found")
    except Exception as e:
        print("Error, incosistent graph specification OR file format is invalid")
        exit()
    
    return graph, continents, t1, t2