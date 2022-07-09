# import streamlit as st 
# import pandas as pd
# import yfinance as yf

# st.write(""" # Data App """)

# st.sidebar.header('User Input')
# selected_year = st.sidebar.selectbox('Year',list(reversed(range(1980, 2022))))

# #web scrapping of stats
# def load_data():

#     google = yf.Ticker('GOOGL')
#     shareholders = google.major_holders
#     st.line_chart(shareholders)

# load_data()















import cv2
img = cv2.imread('prowonks.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, -1, (0,255,0), 2 )



cv2.imshow('Image',img)