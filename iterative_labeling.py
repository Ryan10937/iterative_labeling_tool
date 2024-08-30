import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

if __name__ == '__main__':
    st.title('Hello Streamlit')
    st.streamlit_image_coordinates()
    coords=streamlit_image_coordinates('./dataset/bag (1).jpg')
    
  