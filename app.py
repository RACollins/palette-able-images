import streamlit as st
from PIL import Image, ImageColor
from io import BytesIO

import altair as alt
import numpy as np
import utils


st.title("Palettise an image")

st.subheader("Input image")
img_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])
render_elements = False
if img_file is not None:
    file_details = {
        "Filename": img_file.name,
        "FileType": img_file.type,
        "FileSize": img_file.size,
    }
    st.write(file_details)
    img_original = Image.open(img_file)
    width, height = img_original.size
    image_details = {"Width": "{} px".format(width), "Height": "{} px".format(height)}
    st.write(image_details)
    st.header("Original Image")
    st.image(img_original, use_column_width="auto")
    render_elements = True
else:
    st.info("☝️ Upload a .jpg or .png file")

if render_elements:
    with st.sidebar:
        st.header("Settings")
        colour_var_dict = {}
        nColours = st.number_input(
            "Number of colours",
            value=3,
            placeholder="Type a number...",
            key="nColours",
        )
        img_pbn = utils.reduce_colours(img=img_original, nColours=nColours)
        img_pbn_info_df = utils.get_palette_info(img_pbn)
        default_colours = [utils.rgb2hex(rgb) for rgb in img_pbn_info_df["RGB"].values]
        for c in range(int(nColours)):
            colour_var_dict[c] = st.color_picker(
                f"Colour {c+1}", key=c, value=default_colours[c]
            )

        st.subheader("Resize")
        width = st.number_input(
            "Width (pixels)",
            value=width,
            placeholder="Type a number...",
        )
        height = st.number_input(
            "Height (pixels)",
            value=height,
            placeholder="Type a number...",
        )

        st.subheader("Dither")
        isDither = st.checkbox(
            "Apply dither",
            help="With dither applied, random noise is added to the final image "
            "which helps to smooth harsh edges.",
        )

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
    img_new_palette = utils.quantise_to_palette(
        img=img_resized, palette=new_palette, dither=isDither
    )
    st.header("Palettised Image")
    st.image(img_new_palette, use_column_width="auto")
    img_new_palette_info_df = utils.get_palette_info(img_new_palette)
    st.dataframe(img_new_palette_info_df)

    plot = (
        alt.Chart(img_new_palette_info_df)
        .mark_bar()
        .encode(
            x=alt.X("ColourID"),
            y="Frequency",
            color=alt.Color(
                "ColourID",
                scale=alt.Scale(
                    domain=img_new_palette_info_df["ColourID"].tolist(),
                    range=[
                        utils.rgb2hex(rgb)
                        for rgb in img_new_palette_info_df["RGB"].values
                    ]
                    + ["#00000"],
                ),
            ),
        )
    )
    st.altair_chart(plot, use_container_width=True)


    img_file_name = img_file.name.split(".")[0]
    img_file_type = img_file.name.split(".")[-1]
    
    buf = BytesIO()
    img_new_palette.convert("RGB").save(buf, format=img_file_type.upper())
    byte_img = buf.getvalue()

    # columns to lay out the download buttons
    lower_grid = st.columns(2)

    with lower_grid[0]:
        dwnld_img_btn = st.download_button(
            label="Download Palettised Image",
            data=byte_img,
            file_name="{0}_palettised.{1}".format(img_file_name, img_file_type),
            mime="image/{}".format(img_file_type),
        )
