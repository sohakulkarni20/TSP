from time import perf_counter
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.two_opt import improve_two_opt
from algorithms.brute_force import brute_force
from algorithms.held_karp import held_karp
from core.distance import distance_matrix, route_distance


def run_algorithm(name, cities, animate=False):
    dist = distance_matrix(cities)
    start = perf_counter()

    if name == "Nearest Neighbor":
        route, states = nearest_neighbor(dist)
        optimal = False
        complexity = "O(n²)"
        description = "Repeatedly visit the nearest unvisited city. Fast, but it can miss the global optimum."
    elif name == "Nearest Neighbor + 2-opt":
        route, states = nearest_neighbor(dist)
        route, extra = improve_two_opt(route, dist)
        states += extra
        optimal = False
        complexity = "Typically O(n²) per improvement pass"
        description = "Build a quick tour, then improve it by reversing route segments when that shortens the tour."
    elif name == "Brute Force":
        if len(cities) > 9:
            raise ValueError("Brute Force is limited to 9 cities in this demo.")
        route, states = brute_force(dist)
        optimal = True
        complexity = "O(n!) time; O(n) auxiliary route space (excluding permutations)"
        description = "Enumerate all tours while fixing the first city to avoid equivalent rotations. Guarantees an optimal tour."
    elif name == "Held–Karp DP":
        if len(cities) > 15:
            raise ValueError("Held–Karp is limited to 15 cities in this demo.")
        route, states = held_karp(dist)
        optimal = True
        complexity = "O(n² · 2ⁿ) time and O(n · 2ⁿ) space"
        description = "Dynamic programming stores the best path to each subset of cities and endpoint. Guarantees an optimal tour."
    else:
        raise ValueError(f"Unknown algorithm: {name}")

    elapsed_ms = (perf_counter() - start) * 1000
    return {
        "route": route,
        "distance": route_distance(route, dist),
        "runtime_ms": elapsed_ms,
        "states_explored": states,
        "optimal": optimal,
        "complexity": complexity,
        "description": description
    }
