import pickle
import os

import numpy as np
from skimage.io import imsave

batch_count = 2
batch_folder = "cifar-100-batches"
output_folder = "generated-set"

def main():
    palette = generate_palette(30)

    print("color image set generator v0.1")
    print("batch count: " + str(batch_count))
    print("palette size: " + str(len(palette)))
    print("press ENTER to start")
    input()
    
    if not os.path.exists(f"./{output_folder}"):
            os.makedirs(f"./{output_folder}")

    for b in range(batch_count):
        batch = unpickle_batch(f"./{batch_folder}/data_batch_{b+1}")
        batch_len = len(batch[b"data"])
        filenames = batch[b"filenames"]
        
        for i in range(batch_len):
            image = get_image(batch, i)
            image_color = get_average_color(image)
            closest_color = []
            
            s = 0
            while (closest_color == []):
                for color in palette:
                    if get_color_similarity(image_color, color, 30 + s*10):
                        closest_color = color
                        break
                s += 1
            
            folder = "./generated-set/" + str(closest_color).replace(" ", "_").replace("[", "").replace("]", "").replace(",", "")
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            imsave(f"{folder}/{str(filenames[i])}.png", image)
            
            os.system("clear")
            print(f"Processing batch {b+1} out of {batch_count}");
            print(f" {int((i+1)/batch_len*100)}% [{'='*int((i+1)/batch_len*40)}{' '*int(40-(i+1)/batch_len*40)}] {i+1}/{batch_len}");

# euclidean distance between colors
def get_color_similarity(color1, color2, threshold):
    return np.absolute(np.subtract(color1 , color2)).sum() < threshold
    
# mean color value of image
def get_average_color(image):
    return np.ceil(np.mean(image, axis=(0, 1))).astype(np.uint8)

# extract image data from batch
def get_image(batch, i):
    image = batch.get(b"data")[i]
    red = image[0:1024]
    green = image[1024:2048]
    blue = image[2048:]
    rgb_image = np.empty([0, 32, 3], np.uint8)
    
    for y in range(32):
        x_arr = np.empty([0, 3], np.uint8)
        for x in range(32):
            x_arr = np.append(x_arr, [[red[y*32+x], green[y*32+x], blue[y*32+x]]], 0)
        rgb_image = np.append(rgb_image, [x_arr], 0)
    
    return rgb_image.astype(np.uint8)
   
# generate color categorization palette
def generate_palette(step):
    colors = []
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                colors.append([r, g, b])
    colors.append([255, 255, 255])
    return colors

def unpickle_batch(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
    
main()
