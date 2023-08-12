# Mathematical constants
E = 2.718281828459045  # Euler's number
ATR = 0.017453292519943295  # Degrees to radians conversion factor
COS = 0.9998476951563913  # Approximate cosine value for small angles
SIN = 0.01745240643728351  # Approximate sine value for small angles

def clamp(x, lower, upper):
    """Clamp a value x between lower and upper limits."""
    return max(lower, min(x, upper))
    
def lerp(start, end, t):
    """Linearly interpolate between start and end based on parameter t."""
    return start + (end - start) * t

def smoothstep(start, end, t):
    """Smoothly interpolate between start and end using smoothstep function."""
    t = clamp((t - start) / (end - start), 0.0, 1.0)
    return t * t * (3 - 2 * t)

def smoothstep_angle(angle1, angle2, t):
    """Smoothly interpolate between angle1 and angle2 using smoothstep function."""
    angle_diff = angle2 - angle1
    t_smooth = t * t * (3 - 2 * t)
    interpolated_angle = angle1 + angle_diff * t_smooth
    return interpolated_angle

def remap(value, input_min, input_max, output_min, output_max):
    """Remap a value from the input range to the output range."""
    return output_min + (output_max - output_min) * (value - input_min) / (input_max - input_min)

def lerp_angle(start, end, t):
    """Linearly interpolate between start and end angles."""
    shortest_angle = ((((end - start) % 360) + 540) % 360) - 180
    return start + shortest_angle * t

def distance(obj1, obj2):
    """Calculate the Euclidean distance between two objects with rect attributes."""
    return ((obj2.rect.x - obj1.rect.x) ** 2 + (obj2.rect.y - obj1.rect.y) ** 2) ** 0.5

def rotate_point(x, y, angle):
    """Rotate a point (x, y) by a given angle in degrees."""
    radians = angle * ATR
    cos_angle = COS * radians
    sin_angle = SIN * radians
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle
    return new_x, new_y

def lerp_color(start_color, end_color, t):
    """Linearly interpolate between two RGB colors based on parameter t."""
    r = int(lerp(start_color[0], end_color[0], t))
    g = int(lerp(start_color[1], end_color[1], t))
    b = int(lerp(start_color[2], end_color[2], t))
    return r, g, b

def ease_in(t):
    """Apply ease-in easing function to parameter t."""
    return t * t

def ease_out(t):
    """Apply ease-out easing function to parameter t."""
    return 1 - (1 - t) * (1 - t)

def ease_in_out(t):
    """Apply ease-in-out easing function to parameter t."""
    return t * t * (3 - 2 * t)

def sigmoid(x):
    """Compute the sigmoid function of x."""
    return 1 / (1 + E ** -x)