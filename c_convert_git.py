# To jest wersja 2.0 Konwertera kolorów

import streamlit as st
import cv2
import numpy as np
import os

st.header('Konwerter niebieskich stron zeskanowanych w formie pliku jpg')
up_file = st.file_uploader("Wybierz plik jpg")
if up_file is not None:
    file_name = os.path.splitext(up_file.name)[0]
    # Read the images  
    file_bytes = np.asarray(bytearray(up_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Resizing the image
    image = cv2.resize(img, (1700, 2600))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Defining lower and upper bound HSV values
    lower = np.array([0, 50, 50]) #[0, 50, 50]
    upper = np.array([204, 255, 255]) #[204, 255, 255]

    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)

    # Convert color on the image to black where we found blue
    image[mask>0]=(192,192,192)  #(51,0,0) is black  (192,192,192) light grey
    
    file_name_input = st.text_input('Tutaj możesz wprowadzić dowolną nazwę pliku po konwersji', file_name+'_B.jpg')
    st.write('Nazwa pliku po konwersji to', file_name_input)
    #cv2.imwrite(file_name_input,image)
    #st.subheader('To jest wynik konwersji')
    #st.image(file_name_input)
    #st.download_button('Download gotowej wersji', file_name_input)

    # Convert the processed image back to bytes
    is_success, im_buf_arr = cv2.imencode(".jpg", image)
    byte_im = im_buf_arr.tobytes()
    
    # Display the processed image
    st.subheader('To jest wynik konwersji')
    st.image(byte_im, use_column_width=True)
    
    # Provide a download button for the processed image
    st.download_button('Download gotowej wersji', byte_im, file_name=file_name_input, mime='image/jpeg')

