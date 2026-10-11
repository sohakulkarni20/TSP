def nearest_neighbor(dist, start=0):
    n = len(dist)
    if n == 0:
        return [], 0
    unvisited = set(range(n))
    unvisited.remove(start)
    route = [start]
    states = 0
    current = start

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current][city])
        states += len(unvisited)
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return route, states
