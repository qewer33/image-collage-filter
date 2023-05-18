import numpy as np

# euclidean distance between colors
def get_color_similarity(color1, color2, threshold):
    return np.absolute(np.subtract(color1 , color2)).sum() < threshold
    
# mean color value of image
def get_average_color(image):
    return np.ceil(np.mean(image, axis=(0, 1))).astype(np.uint8)

# generate color categorization palette
def generate_palette(step):
    colors = []
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                colors.append([r, g, b])
    colors.append([255, 255, 255])
    return colors

# get the cclosest color to a color from a palette
def closest_color_from_palette(palette, check_color):
    closest_color = []

    i = 0
    while (closest_color == []):
        for color in palette:
            if get_color_similarity(check_color, color, 30 + i*10):
                closest_color = color
                break
        i += 1

    return closest_color