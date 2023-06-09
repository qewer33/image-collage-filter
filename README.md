![banner](https://github.com/qewer33/image-collage-filter/blob/main/assets/banner.png?raw=true)

`image_collage_filter.py` is a python script that recreates an image as an image made up of smaller 32x32 images (like an image collage but the collage itself is an image). Explaining it is a bit rough, so just try it yourself and see!

## Usage

The script has 3 subcommands:

```bash
# shows the help message
python image_collage_filter.py help
# applies the filter to image.png
python image_collage_filter.py apply ./image.png
# profiles one iteration of the script on image.png
python image_collage_filter.py profile ./image.png
```

Here is an example image (the Hungarian Parliament Building in Budapest) in it's original form:

![parliament](https://github.com/qewer33/image-collage-filter/blob/main/examples/parliament.jpg?raw=true)

And here it is ran trhough the script (download the image and zoom in for _disturbing_ detail):

![parliament_out](https://github.com/qewer33/image-collage-filter/blob/main/examples/parliament_out.png?raw=true)

## Dataset Generation

For the `image_collage_filter.py` script to work, it needs 32x32 images categorized by their average colors. The `cifar_100_preprocessor.py` categorizes CIFAR-100 images by their median colors and exports them to `./generated-set` as png images.

