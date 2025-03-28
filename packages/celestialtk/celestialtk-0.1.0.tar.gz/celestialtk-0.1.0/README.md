# CelestialTK

A Tkinter animation library for creating celestial-like floating points with customizable behavior.

## Installation

```bash
pip install celestialtk
```

## Quick Start

```python
import tkinter as tk
from celestialtk import FloatingPointsAnimator

# Create a tkinter window
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300, bg='black')
canvas.pack()

# Create floating points animator
animator = FloatingPointsAnimator(
    canvas, 
    num_points=50, 
    base_color='#00ffff',  # Cyan points
    fall_direction='down',
    blink_enabled=True
)

root.mainloop()
```

## Features

- Customizable number of points
- Adjustable point sizes
- Multiple falling directions
- Optional blinking effect
- Color and opacity control

## Parameters

- `num_points`: Total number of points (default: 50)
- `sizes`: List of possible circle radii (default: [2, 5])
- `speed_range`: Tuple of (min_speed, max_speed) (default: (1, 5))
- `blink_enabled`: Whether points blink (default: True)
- `fall_direction`: Direction of points ("down", "up", "left", "right", or "random")
- `base_color`: Hex color of points
- `bg_color`: Background color
- `opacity`: Opacity of points (0-1)
- `update_interval`: Animation update interval in ms

## License

MIT License