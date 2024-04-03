import random

def make_color(num_colors):
    colors = []
    for _ in range(num_colors):
        # Generate random RGB values
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        # Format RGB values into a hex color code
        color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        colors.append(color_hex)
    return colors