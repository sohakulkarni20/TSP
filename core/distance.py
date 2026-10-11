import random
import math


def random_cities(count: int, seed: int | None = None):
    """Return deterministic pseudo-random 2D city coordinates in a 0–100 canvas."""
    rng = random.Random(seed)
    points = []
    for _ in range(count):
        # Avoid almost-identical points to make the route easier to see.
        for _attempt in range(100):
            p = (round(rng.uniform(5, 95), 2), round(rng.uniform(5, 95), 2))
            if all(math.dist(p, q) > 7 for q in points):
                points.append(p)
                break
        else:
            points.append((round(rng.uniform(5, 95), 2), round(rng.uniform(5, 95), 2)))
    return points


def distance_matrix(cities):
    n = len(cities)
    return [[math.dist(cities[i], cities[j]) for j in range(n)] for i in range(n)]


def route_distance(route, dist):
    if not route:
        return 0.0
    return sum(dist[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))
