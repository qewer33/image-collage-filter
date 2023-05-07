import sys
import os
import random
import cProfile

from PIL import Image

SET_DIR = "./generated-set"

def main():
    match (sys.argv[1]):
        case "apply":
            if len(sys.argv) < 3:
                print("Please provide an input file")
                exit()
            elif len(sys.argv) < 4:
                in_path = sys.argv[2]
                out_path = in_path + "_out.png"
            else:
                in_path = sys.argv[2]
                out_path = sys.argv[3]

            apply_filter(in_path, out_path)
            pass
        case "profile":
            if len(sys.argv) < 3:
                print("Please provide an input file")
                exit()
            elif len(sys.argv) < 4:
                in_path = sys.argv[2]
                iter_count = 1
            else:
                in_path = sys.argv[2]
                iter_count = int(sys.argv[3])
            
            cProfile.run(f"apply_filter('{in_path}', True, {iter_count})")
        case "help":
            print("image-collage-filter.py rev1")
            print()
            print("Available commands:")
            print("  apply {in_path} {out_path = in_path + '_out.png'}")
            print("    Applies the filter to the image in the given in_path and saves it to the out_path. If out_path is not specified, the image is saved to in_path appended with '_out.png'.")
            print()
            print("  profile {in_path} {iter_count = 1}")
            print("    Profiles the script on the given image with the given iteration count. Mainly for debugging purposes.")
            print()
            print("  help")
            print("    Shows this help message.")
            print()
            print("Example usage:")
            print("  python image-collage-filter.py apply ./examples/parliament.png")
            print("  python image-collage-filter.py apply ./examples/landscape.jpg landscape_out.png")

# apply filter to the image given path and save it to te output path
def apply_filter(in_path, out_path, profile=False, profile_iter_count=1):
    palette = [x[0] for x in os.walk(SET_DIR)]
    palette.pop(0)
    palette = list(map(lambda x: (list(map(int, x.replace(SET_DIR + "/", "").split("_"))), x, os.listdir(x)), palette))
    input_str = sys.argv[1]
    profile_iter = 0
    
    with Image.open(in_path) as img:
        out_img = Image.new("RGB", img.size)
        
        for y in range(0, img.height, 32):
            for x in range(0, img.width, 32):
                color = img.getpixel((x, y))
                # area = img.copy().crop((x, y, x+32, y+32))
                # color = get_average_color(area.getcolors())
                
                for p in palette:
                    if get_color_similarity(p[0], color, 50):
                        path = f"{p[1]}/{random.choice(p[2])}"
                        out_img.paste(Image.open(path), (x, y))
                        break

                profile_iter += 1
                if profile and profile_iter == profile_iter_count:
                    return
                
                
        out_img.show()
        out_img.save(out_path)
        
# euclidean distance between colors
def get_color_similarity(color1, color2, threshold):
    return sum(list(map(lambda x, y: abs(x - y), color1, color2))) < threshold
    
# mean color value of image
# needs optimization
def get_average_color(colors):
    red = []
    green = []
    blue = []
    for c in colors:
        red.append(c[1][0])
        green.append(c[1][1])
        blue.append(c[1][2])
    return [sum(red)/len(red), sum(green)/len(green), sum(blue)/len(blue)]

main()
