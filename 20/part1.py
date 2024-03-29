from collections import defaultdict
from heapq import heappop, heappush

start = None
stop = None

def search_labels(map):
    maze_chars = ' .#'
    y_size = len(map)
    x_size = len(map[0].strip('\n'))

    label_positions = set()
    labels = list()

    for y in range(y_size):
        for x in range(x_size):
            if (x, y) in label_positions:
                continue
            if map[y][x] not in maze_chars:
                label_positions.add((x, y))
                label = map[y][x]
                if map[y + 1][x] not in maze_chars:
                    # Vertical label
                    label_positions.add((x, y+1))
                    label += map[y+1][x]
                    for portal_y in [y-1, y+2]:
                        if portal_y > 0 and portal_y < y_size:
                            if map[portal_y][x] == '.':
                                labels.append((label, (x, portal_y)))
                                break
                else:
                    # Horizontal label
                    label_positions.add((x+1, y))
                    label += map[y][x+1]
                    for portal_x in [x-1, x+2]:
                        if portal_x > 0 and portal_x < x_size:
                            if map[y][portal_x] == '.':
                                labels.append((label, (portal_x, y)))
                                break
    return labels

def shortest_path(maze_map, a, b, links):
        '''Find shortest path between a and b. Returns the steps needed.'''
        
        def get_next(position):
            directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            x, y = position
            yield from ((x + d[0], y + d[1]) for d in directions if maze_map[y + d[1]][x + d[0]] == '.')
            if position in links:
                yield links[position]
        def distance(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - b[0])

        cache = dict()
        if (a, b) in cache:
            return cache[(a,b)] 
        frontier = []
        come_from = {}
        cost_to = {}
        heappush(frontier, (0, a))
        come_from[a] = None
        cost_to[a] = 0

        while len(frontier) > 0:
            current = heappop(frontier)[1]

            if current == b:
                break

            for next_point in get_next(current):
                new_cost = cost_to[current] + 1
                if next_point not in cost_to or new_cost < cost_to[next_point]:
                    cost_to[next_point] = new_cost
                    priority = new_cost + 0 #distance(next_point, b)
                    heappush(frontier, (priority, next_point))
                    come_from[next_point] = current
        else:
            return None
        
        cache[(a, b)] = cost_to[b]
        return cost_to[b]

with open('20/test3') as f:
    raw_map = f.readlines()
    labels = search_labels(raw_map)
    
    portals_by_label = defaultdict(list)
    
    for label, position in labels:
        if label == 'AA':
            start = position
        elif label == 'ZZ':
            stop = position
        else:
            portals_by_label[label].append(position)
    
    portals = dict()

    for label in portals_by_label:
        p1, p2 = portals_by_label[label]
        portals[p1] = p2
        portals[p2] = p1

    print(shortest_path(raw_map, start, stop, portals))

    
