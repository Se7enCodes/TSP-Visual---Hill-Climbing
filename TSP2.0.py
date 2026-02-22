import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button

# --- Setup ---
N = 50
np.random.seed(42)
cities = np.random.rand(N, 2)
# For 2-Dimensional space

def total_distance(route):
    d = 0
    for i in range(len(route)):
        a, b = cities[route[i]], cities[route[(i+1) % len(route)]]
        d += np.linalg.norm(a - b)
    return d

def two_opt_swap(route):
    r = route.copy()
    i, j = sorted(np.random.choice(len(r), 2, replace=False))
    r[i:j+1] = r[i:j+1][::-1]
    return r

# --- State ---
# Randomly initialised travelling route, no intelligence.
current = list(np.random.permutation(N))
current_dist = total_distance(current)
best_dist = current_dist

distance_history = [current_dist]
iteration = [0]
stuck_counter = [0]          # how many consecutive failed swaps
STUCK_THRESHOLD = 50        # declare local optima after this many failed attempts
is_global = [False]
local_optima_distances = []  # to compare against

# --- Figure Layout ---
fig = plt.figure(figsize=(12, 6))
gs = GridSpec(2, 2, figure=fig, width_ratios=[2, 1])

ax_route = fig.add_subplot(gs[:, 0])   # route (full left column)
ax_dist  = fig.add_subplot(gs[0, 1])   # distance over time
ax_info  = fig.add_subplot(gs[1, 1])   # text info panel

ax_route.set_xlim(-0.05, 1.05)
ax_route.set_ylim(-0.05, 1.05)
ax_route.set_title("TSP - Hill Climbing", fontsize=13)
ax_route.scatter(cities[:, 0], cities[:, 1], c='red', zorder=5, s=60)

ax_dist.set_title("Distance over Iterations")
ax_dist.set_xlabel("Iteration")
ax_dist.set_ylabel("Distance")

ax_info.axis('off')

# Route line
line, = ax_route.plot([], [], 'b-o', lw=1.5, markersize=4)

# Status badge (top-left of route plot)
status_text = ax_route.text(
    0.02, 0.97, "", transform=ax_route.transAxes,
    fontsize=11, verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='gray', alpha=0.85)
)

# Distance history line
dist_line, = ax_dist.plot([], [], 'b-', lw=1.5)
ax_dist.set_xlim(0, 300)

# Info text box
info_text = ax_info.text(
    0.05, 0.95, "", transform=ax_info.transAxes,
    fontsize=10, verticalalignment='top', family='monospace',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#f7f7f7', edgecolor='#cccccc')
)

def get_status():
    # Blue while improving, orangle while searching, red at local optimum, green if it's best local optimum found so far (global within the run)
    """Determine if we're improving, at local optima, or global optima."""
    if stuck_counter[0] == 0:
        return "improving", "🔼 Improving", "#d4edda", "#155724"
    elif stuck_counter[0] < STUCK_THRESHOLD:
        return "searching", f"↔ Searching ({stuck_counter[0]})", "#fff3cd", "#856404"
    else:
        # local or global?
        if is_global[0]:
            return "global", "★ Global Optimum", "#cce5ff", "#004085"
        else:
            return "local", "⚠ Local Optimum", "#f8d7da", "#721c24"

def init():
    line.set_data([], [])
    dist_line.set_data([], [])
    return line, dist_line, status_text, info_text

def update(frame):
    global current, current_dist, best_dist

    improved = False
    for _ in range(10):
        neighbor = two_opt_swap(current)
        nd = total_distance(neighbor)
        if nd < current_dist:
            # Reason for monotonic non-increasin nature
            current, current_dist = neighbor, nd
            stuck_counter[0] = 0
            improved = True
            if current_dist < best_dist:
                best_dist = current_dist
                is_global[0] = False  # reset; we found something better
        else:
            stuck_counter[0] += 1

    iteration[0] += 1
    distance_history.append(current_dist)

    # Check if this is truly the global best seen so far
    if stuck_counter[0] >= STUCK_THRESHOLD:
        if not local_optima_distances or current_dist < min(local_optima_distances):
            is_global[0] = True
        else:
            is_global[0] = False
        if not local_optima_distances or not any(abs(current_dist - d) < 1e-6 for d in local_optima_distances):
            local_optima_distances.append(current_dist)

    # --- Route plot ---
    route = current + [current[0]]
    x = cities[route, 0]
    y = cities[route, 1]
    line.set_data(x, y)

    # Route color based on status
    status, label, bg, fg = get_status()
    colors = {"improving": "royalblue", "searching": "darkorange", 
              "local": "crimson",      "global": "mediumseagreen"}
    line.set_color(colors[status])

    # Status badge
    status_text.set_text(label)
    status_text.get_bbox_patch().set_facecolor(bg)
    status_text.set_color(fg)

    # --- Distance plot ---
    iters = list(range(len(distance_history)))
    dist_line.set_data(iters, distance_history)
    ax_dist.set_xlim(0, max(300, len(distance_history)))
    ax_dist.set_ylim(
        min(distance_history) * 0.95,
        max(distance_history) * 1.05
    )

    # --- Info panel (tracker) ---
    # Tracks iteration cnt, current and best dist, overall % improvement, failed swaps (consecutive), number of distinct local optima found
    info_text.set_text(
        f"  Iteration   : {iteration[0]}\n"
        f"  Curr Dist   : {current_dist:.4f}\n"
        f"  Best Dist   : {best_dist:.4f}\n"
        f"  Improvement : {((distance_history[0] - best_dist) / distance_history[0] * 100):.1f}%\n"
        f"  Stuck for   : {stuck_counter[0]} iters\n"
        f"  Local optima: {len(local_optima_distances)} found"
    )

    return line, dist_line, status_text, info_text

ani = animation.FuncAnimation(
    fig, update, frames=150,
    init_func=init, interval=40, blit=True
)

def restart(event):
    global current, current_dist, best_dist
    current = list(np.random.permutation(N))
    current_dist = total_distance(current)
    distance_history.clear()
    distance_history.append(current_dist)
    iteration[0] = 0
    stuck_counter[0] = 0
    ani.event_source.start()   # un-stops the animation if it was halted

ax_button = plt.axes([0.45, 0.01, 0.1, 0.04])
btn = Button(ax_button, 'Restart')
btn.on_clicked(restart)

plt.tight_layout()
plt.show()