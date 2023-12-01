import streamlit as st
from PIL import Image, ImageColor

import altair as alt
import numpy as np
import pandas as pd

# import cv2

#################
### Functions ###
#################


def quantise_to_palette(img, palette):
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
    return img.convert("RGB").quantize(palette=p)


def get_palette_info(img):
    palette_colours = img.getcolors()
    imgRGB = img.convert("RGB")
    rgb_colours = imgRGB.getcolors()
    # palette_info_dict = {c: [] for c in ["ColourID", "Frequency", "r", "g", "b"]}
    palette_info_dict = {c: [] for c in ["ColourID", "Frequency", "RGB"]}
    for palette_freq, palette_colour in palette_colours:
        for rgb_freq, rgb_colour in rgb_colours:
            if palette_freq != rgb_freq:
                continue
            palette_info_dict["ColourID"].append("Colour {}".format(palette_colour))
            palette_info_dict["Frequency"].append(rgb_freq)
            palette_info_dict["RGB"].append(
                (rgb_colour[0], rgb_colour[1], rgb_colour[2])
            )
    palette_info_df = pd.DataFrame(palette_info_dict)
    return palette_info_df


st.title("Palettise an image")

st.subheader("Input image")
img_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

if img_file is not None:
    file_details = {
        "Filename": img_file.name,
        "FileType": img_file.type,
        "FileSize": img_file.size,
    }
    st.write(file_details)
    img_original = Image.open(img_file)
    st.text("Original Image")
    st.image(img_original, use_column_width=True)
else:
    st.info("☝️ Upload a .jpg or .png file")


with st.sidebar.form("sidebbar_form"):
    st.header("Settings")
    colour_var_dict = {}
    nColours = st.number_input(
        "Number of colours", value=3, placeholder="Type a number..."
    )
    for c in range(int(nColours)):
        colour_var_dict[c] = st.color_picker(f"Colour {c+1}", key=c)

    width, height = img_original.size
    st.subheader("Resize")
    width = st.number_input(
        "Width (pixels)", value=width, placeholder="Type a number..."
    )
    height = st.number_input(
        "Height (pixels)", value=height, placeholder="Type a number..."
    )
    palettise = st.form_submit_button("Palettise")

if palettise:
    img_resized = img_original.resize((width, height))
    # image_pbn = resized.convert("P", palette=Image.ADAPTIVE, colors=nColours)

    new_palette = list(
        np.array(
            [
                list(ImageColor.getcolor(hex, "RGB"))
                for c, hex in colour_var_dict.items()
            ]
        ).flatten()
    )
    img_new_palette = quantise_to_palette(img=img_resized, palette=new_palette)
    st.image(img_new_palette, use_column_width=True)
    img_new_palette_info_df = get_palette_info(img_new_palette)
    st.dataframe(img_new_palette_info_df)

    plot = (
        alt.Chart(img_new_palette_info_df)
        .mark_bar()
        .encode(
            x=alt.X("ColourID", sort="y"),
            y="Frequency",
            color=alt.Color(
                "ColourID",
                scale=alt.Scale(
                    domain=img_new_palette_info_df["ColourID"].tolist(),
                    range=[
                        "red",
                        "green",
                        "blue",
                        "black",
                    ],
                ),
            ),
        )
    )
    st.altair_chart(plot, use_container_width=True)
    print(img_new_palette_info_df)
