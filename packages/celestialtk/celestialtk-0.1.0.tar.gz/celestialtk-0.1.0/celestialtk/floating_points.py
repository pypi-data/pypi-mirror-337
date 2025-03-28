import tkinter as tk
import random

def blend_colors(fg_hex, bg_hex, opacity):
    """
    Simulates opacity by blending the base color (fg) with the background color (bg).
    Both colors must be in hexadecimal format ("#RRGGBB") and opacity is a value between 0 and 1.
    """
    fg = tuple(int(fg_hex[i:i+2], 16) for i in (1, 3, 5))
    bg = tuple(int(bg_hex[i:i+2], 16) for i in (1, 3, 5))
    blended = tuple(int(bg[i]*(1-opacity) + fg[i]*opacity) for i in range(3))
    return "#%02x%02x%02x" % blended

class FloatingPointsAnimator:
    def __init__(self, canvas, **kwargs):
        """
        Configurable parameters for celestial floating points animation.
        
        Parameters:
        - canvas: Tkinter Canvas where the animation will be drawn
        - num_points: Total number of points (default: 50)
        - sizes: List of possible circle radii (default: [2, 5])
        - speed_range: Tuple (min_speed, max_speed) for speed (default: (1, 5))
        - blink_enabled: Whether points blink (default: True)
        - blink_interval_range: Tuple (min_interval, max_interval) in ms (default: (300, 1000))
        - fall_direction: Falling direction: "down", "up", "left", "right" or "random" (default: "down")
        - base_color: Base point color in hex (default: "#ffffff")
        - bg_color: Canvas background color in hex (default: "#000000")
        - opacity: Opacity value between 0 and 1 (default: 1.0)
        - update_interval: Animation update interval in ms (default: 50)
        """
        self.canvas = canvas
        self.canvas_width = float(canvas['width'])
        self.canvas_height = float(canvas['height'])
        
        # Set default parameters with kwargs
        self.num_points = kwargs.get('num_points', 50)
        self.sizes = kwargs.get('sizes', [2, 5])
        self.speed_range = kwargs.get('speed_range', (1, 5))
        self.blink_enabled = kwargs.get('blink_enabled', True)
        self.blink_interval_range = kwargs.get('blink_interval_range', (300, 1000))
        self.fall_direction = kwargs.get('fall_direction', 'down')
        self.base_color = kwargs.get('base_color', "#ffffff")
        self.bg_color = kwargs.get('bg_color', "#000000")
        self.opacity = kwargs.get('opacity', 1.0)
        self.dt = kwargs.get('update_interval', 50)
        
        # Calculate effective color applying opacity
        self.effective_color = blend_colors(self.base_color, self.bg_color, self.opacity)
        self.points = []
        self._create_points()
        self._animate()

    def _create_points(self):
        """Creates points with their attributes and initial positions."""
        for _ in range(self.num_points):
            radius = random.choice(self.sizes)
            # Assign individual direction if "random" is requested
            if self.fall_direction == "random":
                direction = random.choice(["down", "up", "left", "right"])
            else:
                direction = self.fall_direction
            
            # Initial position based on direction:
            if direction in ["down", "up"]:
                x = random.uniform(radius, self.canvas_width - radius)
                y = random.uniform(0, self.canvas_height)
            else:  # left or right
                x = random.uniform(0, self.canvas_width)
                y = random.uniform(radius, self.canvas_height - radius)
            
            item = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                           fill=self.effective_color, outline=self.effective_color)
            speed = random.uniform(self.speed_range[0], self.speed_range[1])
            blink_on = True
            blink_interval = random.uniform(self.blink_interval_range[0], self.blink_interval_range[1])
            blink_timer = 0
            self.points.append({
                "id": item,
                "speed": speed,
                "radius": radius,
                "blink_on": blink_on,
                "blink_interval": blink_interval,
                "blink_timer": blink_timer,
                "direction": direction
            })

    def _animate(self):
        """Updates animation: blinking, movement, and repositioning."""
        for point in self.points:
            # Blinking update
            if self.blink_enabled:
                point["blink_timer"] += self.dt
                if point["blink_timer"] >= point["blink_interval"]:
                    point["blink_on"] = not point["blink_on"]
                    point["blink_timer"] = 0
                    color = self.effective_color if point["blink_on"] else self.bg_color
                    self.canvas.itemconfig(point["id"], fill=color, outline=color)
            
            # Movement based on assigned direction
            dx, dy = 0, 0
            direction = point["direction"]
            if direction == "down":
                dy = point["speed"]
            elif direction == "up":
                dy = -point["speed"]
            elif direction == "left":
                dx = -point["speed"]
            elif direction == "right":
                dx = point["speed"]
            self.canvas.move(point["id"], dx, dy)
            
            # Reposition when point leaves the area
            coords = self.canvas.coords(point["id"])  # [x1, y1, x2, y2]
            x1, y1, x2, y2 = coords
            radius = point["radius"]
            if direction == "down" and y1 > self.canvas_height:
                new_x = random.uniform(radius, self.canvas_width - radius)
                self.canvas.coords(point["id"], new_x - radius, -radius, new_x + radius, radius)
            elif direction == "up" and y2 < 0:
                new_x = random.uniform(radius, self.canvas_width - radius)
                self.canvas.coords(point["id"], new_x - radius, self.canvas_height - radius,
                                    new_x + radius, self.canvas_height + radius)
            elif direction == "left" and x2 < 0:
                new_y = random.uniform(radius, self.canvas_height - radius)
                self.canvas.coords(point["id"], self.canvas_width - radius, new_y - radius,
                                    self.canvas_width + radius, new_y + radius)
            elif direction == "right" and x1 > self.canvas_width:
                new_y = random.uniform(radius, self.canvas_height - radius)
                self.canvas.coords(point["id"], -radius, new_y - radius, radius, new_y + radius)
        self.canvas.after(self.dt, self._animate)