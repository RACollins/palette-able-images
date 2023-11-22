import streamlit as st
from PIL import Image

# from matplotlib import pyplot as plt
# import numpy as np
# import pandas as pd
# import cv2

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
    original = Image.open(img_file)
    st.text("Original Image")
    st.image(original, use_column_width=False)
else:
    st.info("☝️ Upload a .jpg or .png file")

st.sidebar.header("Settings")

colour_var_dict = {}
nColours = st.sidebar.number_input(
    "Number of colours", value=None, placeholder="Type a number..."
)
for c in range(int(nColours)):
    colour_var_dict[c] = st.sidebar.color_picker(f"Colour {c+1}", key=c)

for k, v in colour_var_dict.items():
    st.write(f"{k}: {v}")
user_food = st.sidebar.selectbox(
    "What is your favorite food?",
    ["", "Tom Yum Kung", "Burrito", "Lasagna", "Hamburger", "Pizza"],
)
