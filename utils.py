from PIL import Image
import pandas as pd

#################
### Functions ###
#################


def reduce_colours(img, nColours):
    image_pbn = img.convert("P", palette=Image.ADAPTIVE, colors=nColours)
    return image_pbn


def quantise_to_palette(img, palette, dither):
    """Quantize image to a given palette.

    The input image is expected to be a PIL Image.
    The palette is expected to be a list of no more than 256 R,G,B values."""

    e = len(palette)
    assert e > 0, "Palette unexpectedly short"
    assert e <= 768, "Palette unexpectedly long"
    assert e % 3 == 0, "Palette not multiple of 3, so not RGB"

    # Make tiny, 1x1 new palette image
    p = Image.new("P", (1, 1))

    # Zero-pad the palette to 256 RGB colours, i.e. 768 values and apply to image
    palette += (768 - e) * [0]
    p.putpalette(palette)

    # Now quantize input image to the same palette as our little image
    return img.convert("RGB").quantize(palette=p, dither=dither)


def get_palette_info(img):
    palette_colours = img.getcolors()
    imgRGB = img.convert("RGB")
    rgb_colours = imgRGB.getcolors()
    palette_info_dict = {c: [] for c in ["ColourID", "Frequency", "RGB"]}
    for palette_freq, palette_colour in palette_colours:
        for rgb_freq, rgb_colour in rgb_colours:
            if palette_freq != rgb_freq:
                continue
            palette_info_dict["ColourID"].append("Colour {}".format(palette_colour + 1))
            palette_info_dict["Frequency"].append(rgb_freq)
            palette_info_dict["RGB"].append(
                (rgb_colour[0], rgb_colour[1], rgb_colour[2])
            )
    palette_info_df = pd.DataFrame(palette_info_dict)
    return palette_info_df


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def hex2rgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode("hex")))
