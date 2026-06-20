import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
df = pd.read_csv(r"C:\Users\macad\Downloads\Bonsai_project\Data\Tree_data.csv")


# Optional: import adjustText if installed
try:
    from adjustText import adjust_text
    HAS_ADJUST = True
except Exception:
    HAS_ADJUST = False

# --- Color map: green (slow growth) → amber → coral (fast growth) ---
growth_cmap = LinearSegmentedColormap.from_list(
    'growth', ['#3b6911', '#639922', '#97c459', '#eaa724', '#d85a30']
)

fig, ax = plt.subplots(figsize=(14, 8))

# --- Sun background gradient (left = cool blue, right = warm yellow) ---
x_min, x_max = 4.5, 11.4
y_min, y_max = 1.5, 11.5

gradient = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(
    gradient,
    aspect='auto',
    extent=[x_min, x_max, y_min, y_max],
    origin='lower',
    cmap=LinearSegmentedColormap.from_list('sun', ['#b0c8e8', '#fff8a0']),
    alpha=0.45,
    zorder=0,
)

# --- Bubble scatter ---
scatter = ax.scatter(
    df['Sun'],
    df['Water'],
    s=df['Wind'] * 120,
    c=df['Growth'],
    cmap=growth_cmap,
    vmin=1, vmax=10,
    alpha=0.88,
    edgecolors='black',
    linewidths=0.8,
    zorder=3,
)

# --- Prepare label positions to avoid stacking ---
# Round coordinates to a small grid to detect near-duplicates
coords = np.column_stack((df['Sun'].round(3).values, df['Water'].round(3).values))

# Map each unique coordinate to indices
unique_map = {}
for idx, (x, y) in enumerate(coords):
    key = (float(x), float(y))
    unique_map.setdefault(key, []).append(idx)

# Compute radial offsets for duplicates
label_offsets = np.zeros((len(df), 2))
for key, indices in unique_map.items():
    n = len(indices)
    if n == 1:
        continue
    # Spread labels on a small circle; radius scales with number of duplicates
    radius = 0.12 + 0.06 * min(n, 8)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    for i, idx in enumerate(indices):
        dx = radius * np.cos(angles[i])
        dy = radius * np.sin(angles[i])
        label_offsets[idx] = [dx, dy]

# --- Labels with adjustText to prevent overlap ---
texts = []
arrows = []
moved_flags = []

for i, row in df.iterrows():
    x = row['Sun']
    y = row['Water']
    dx, dy = label_offsets[i]
    # initial label position (may be adjusted by adjustText)
    text_obj = ax.text(
        x + dx, y + dy, row['Tree'],
        fontsize=8.5,
        zorder=4,
        ha='center',
        va='center',
        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1.2)
    )
    # add subtle outline for readability
    text_obj.set_path_effects([path_effects.Stroke(linewidth=1.2, foreground='white'), path_effects.Normal()])
    texts.append(text_obj)
    # record whether we initially offset the label (used for arrow decisions)
    moved_flags.append((dx != 0) or (dy != 0))

# Use adjustText if available to further reduce overlaps
if HAS_ADJUST:
    try:
        adjust_text(
            texts,
            x=df['Sun'].values,
            y=df['Water'].values,
            ax=ax,
            arrowprops=dict(arrowstyle='-', color='#888888', lw=0.6),
            expand_points=(1.2, 1.6),
            expand_text=(1.1, 1.3),
            force_points=(0.2, 0.3),
            force_text=(0.3, 0.4),
            only_move={'points':'y', 'text':'xy'},
            precision=0.5,
        )
    except Exception:
        # If adjustText fails for any reason, fall back to simple offsets
        for t, (x, y), (dx, dy) in zip(texts, coords, label_offsets):
            t.set_position((x + dx, y + dy))
else:
    # Fallback: ensure labels are offset from points and draw light connector lines for those moved
    for t, (x, y), (dx, dy), moved in zip(texts, coords, label_offsets, moved_flags):
        if moved:
            t.set_position((x + dx, y + dy))
            # draw a subtle connector line
            ax.plot([x, x + dx], [y, y + dy], color='#888888', lw=0.6, zorder=2, alpha=0.7)

# --- Colorbar for growth ---
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Growth rate  (1 = slowest, 10 = fastest)', fontsize=10)
cbar.ax.tick_params(labelsize=9)

# --- Sun gradient legend patch ---
sun_patch = mpatches.Patch(
    facecolor='#fff8a0', edgecolor='#b0c8e8', label='Background: more sunlight →'
)
wind_patch = mpatches.Patch(
    facecolor='#aaaaaa', edgecolor='black', alpha=0.6, label='Bubble size = wind tolerance'
)
ax.legend(handles=[sun_patch, wind_patch], fontsize=8.5, loc='upper left', framealpha=0.7)

# --- Axes & labels ---
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('Sunlight (hours/day)', fontsize=11)
ax.set_ylabel('Water tolerance  (1 = dry, 10 = swamp)', fontsize=11)
ax.set_title('Bonsai Master Placement & Care Guide', fontsize=15, fontweight='medium', pad=14)
ax.grid(True, alpha=0.15, zorder=1)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('bonsai_chart.png', dpi=150, bbox_inches='tight')
plt.show()
