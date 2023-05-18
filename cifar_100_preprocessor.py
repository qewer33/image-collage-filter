import pickle
import os

import numpy as np
from skimage.io import imsave

import preprocess_common as com

BATCH_COUNT = 2
BATCH_FOLDER = "cifar-100-batches"
OUTPUT_FOLDER = "generated-set"

def main():
    palette = com.generate_palette(30)

    print("color image set generator v0.1")
    print("batch count: " + str(BATCH_COUNT))
    print("palette size: " + str(len(palette)))
    print("press ENTER to start")
    input()
    
    if not os.path.exists(f"./{OUTPUT_FOLDER}"):
            os.makedirs(f"./{OUTPUT_FOLDER}")

    for b in range(BATCH_COUNT):
        batch = unpickle_batch(f"./{BATCH_FOLDER}/data_batch_{b+1}")
        batch_len = len(batch[b"data"])
        filenames = batch[b"filenames"]
        
        for i in range(batch_len):
            image = get_image(batch, i)
            image_color = com.get_average_color(image)
            closest_color = com.closest_color_from_palette(palette, image_color)
            
            folder = f'./{OUTPUT_FOLDER}/{str(closest_color).replace(" ", "_").replace("[", "").replace("]", "").replace(",", "")}'
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            imsave(f"{folder}/{str(filenames[i])}.png", image)
            
            os.system("clear")
            print(f"Processing batch {b+1} out of {BATCH_COUNT}");
            print(f" {int((i+1)/batch_len*100)}% [{'='*int((i+1)/batch_len*40)}{' '*int(40-(i+1)/batch_len*40)}] {i+1}/{batch_len}");

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

def unpickle_batch(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
    
main()
