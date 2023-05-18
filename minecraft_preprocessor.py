import os

import numpy as np
from skimage.io import imsave, imread
from skimage.color import rgba2rgb

import preprocess_common as com

SET_DIR = "./datasets/minecraft_textures"
OUTPUT_FOLDER = "generated-set-minecraft"

def main():
    palette = com.generate_palette(30)

    if not os.path.exists(f"./{OUTPUT_FOLDER}"):
            os.makedirs(f"./{OUTPUT_FOLDER}")

    for folder in list(os.walk(SET_DIR)):
        print(folder[0])
        for files in folder[1:]:
            for file in files:
                if file[-4:] == ".png":
                    image = imread(folder[0] + "/" + file)
                    image = rgba2rgb(image).astype(np.uint8)
                    image_color = com.get_average_color(image)
                    closest_color = com.closest_color_from_palette(palette, image_color)

                    folder = f'./{OUTPUT_FOLDER}/{str(closest_color).replace(" ", "_").replace("[", "").replace("]", "").replace(",", "")}'
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                        
                    imsave(f"{folder[0]}/{file}", image)

main()