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
