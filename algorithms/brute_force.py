from itertools import permutations


def brute_force(dist):
    n = len(dist)
    if n <= 1:
        return list(range(n)), 1
    best_route = None
    best_distance = float("inf")
    states = 0

    # Fix city 0; all rotations of a tour are equivalent.
    for tail in permutations(range(1, n)):
        route = (0,) + tail
        total = sum(dist[route[i]][route[i + 1]] for i in range(n - 1))
        total += dist[route[-1]][route[0]]
        states += 1
        if total < best_distance:
            best_distance = total
            best_route = list(route)

    return best_route, states
