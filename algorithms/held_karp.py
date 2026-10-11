def held_karp(dist):
    """Exact TSP via bitmask DP, fixing city 0 as the start."""
    n = len(dist)
    if n <= 1:
        return list(range(n)), 1

    # DP[(mask, j)] = best path cost from 0 through mask, ending at j.
    # Bits represent cities 1..n-1.
    dp = {}
    parent = {}
    states = 0

    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[(mask, j)] = dist[0][j]
        parent[(mask, j)] = 0
        states += 1

    full_mask = (1 << (n - 1)) - 1
    for mask in range(1, full_mask + 1):
        for j in range(1, n):
            j_bit = 1 << (j - 1)
            if not (mask & j_bit) or (mask == j_bit):
                continue
            prev_mask = mask ^ j_bit
            best_cost = float("inf")
            best_prev = None
            for k in range(1, n):
                k_bit = 1 << (k - 1)
                if prev_mask & k_bit:
                    cost = dp[(prev_mask, k)] + dist[k][j]
                    if cost < best_cost:
                        best_cost, best_prev = cost, k
            dp[(mask, j)] = best_cost
            parent[(mask, j)] = best_prev
            states += 1

    end_city = min(range(1, n), key=lambda j: dp[(full_mask, j)] + dist[j][0])
    best_total = dp[(full_mask, end_city)] + dist[end_city][0]

    reverse_route = [end_city]
    mask = full_mask
    current = end_city
    while current != 0:
        previous = parent[(mask, current)]
        mask ^= 1 << (current - 1)
        current = previous
        if current != 0:
            reverse_route.append(current)

    route = [0] + list(reversed(reverse_route))
    return route, states
