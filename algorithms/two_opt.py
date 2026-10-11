from core.distance import route_distance


def improve_two_opt(route, dist):
    """Improve a tour with first-improvement 2-opt; return route and candidate count."""
    best = route[:]
    n = len(best)
    candidates = 0
    improved = True

    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                candidates += 1
                if k - i == 1:
                    continue
                candidate = best[:i] + best[i:k + 1][::-1] + best[k + 1:]
                if route_distance(candidate, dist) + 1e-9 < route_distance(best, dist):
                    best = candidate
                    improved = True
                    break
            if improved:
                break

    return best, candidates
