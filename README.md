# Core Idea - TRAVELLING SALESMAN PROBLEM

You have N cities plotted as points. A solution is a route (permutation of cities). The fitness is total route distance. Hill climbing tries random swaps and keeps them only if they shorten the route (total cost).

    -> The visualization just redraws the route after every accepted swap.

# Animate -
    Each frame = one iteration. We redraw:

        The city points (static)
        The current route as connected lines
        A live counter showing total distance decreasing
        Optionally highlight the two edges being swapped in red before accepting/rejecting


# Visualization:


What Happens Visually
Early frames — the route looks like a tangled mess of crossing lines. As the algorithm runs, crossings disappear and the route tightens up. Then it stops improving even though the route isn't perfect — that's your local optimum moment, and it's the whole point of the demo.

# Upgrades:
    * Add a "restart from random" button to show it finds a different local optimum each time
    <!-- * Plot distance over time in a second subplot — the curve flattening out visually shows convergence -->
    <!-- * Color the route from blue → green as it improves -->
    * Compare hill climbing side-by-side with random search to show it's actually doing something intelligent

# Findings:
    1. With each restart, the converging value (best_dist) comes out to be more or less than before. This shows that in hill climbing algorithm, the goal state depends on the initial state.
    
    2. The algorithm has no memory of previous runs and no global view of the search space. It only knows its current position and its immediate neighbors. So wherever you drop it, it climbs to the nearest peak and stops — completely unaware that a higher peak exists elsewhere.
    
    3. This is why it's called a local search algorithm. It's not searching the space, it's just sliding uphill from wherever it started.