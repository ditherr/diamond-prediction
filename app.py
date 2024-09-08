import os
import pandas as pd
import numpy as np
import streamlit as st
from src.pipeline.predict_pipeline import CustomDataPrice, CustomDataCarat, PredictPipeline

## Dataset
dataset = pd.read_csv('data/diamonds.csv')

text_header = """:wave: Welcome to **Diamond P&C Prediction**:wave:
                
:bar_chart: You can **predict the ideal :blue-background[price] or :blue-background[weight] of the 💎**

Hopefully, you can get the **fine choice for the 💎 that you've ever dream of!**:cloud:
"""


def main():
    st.set_page_config(
        page_title="Diamond Prediction",
        page_icon="💎",
        layout="centered"
    )
    
    st.title("💎Diamond **P&C** Prediction💎")
    st.markdown(text_header)
    
    tab1, tab2, tab3 = st.tabs(["🗃 Dataset", "💵 Predict Price", "💎 Predict Carat"])
    
    with tab1:
        st.subheader('📋Existing Dataset')
        dataset.columns = ['Carat', 'Cut', 'Color', 'Clarity', 'Depth', 'Table', 'Price', 'x', 'y', 'z']
        st.write(dataset)
    
    # Price
    with tab2:
        st.subheader("🔎Do the Weight Prediction")
        st.caption("**I guest, you already know what :blue[type and size] of :gem: that you need!**")
        with st.form('Diamond Price', clear_on_submit=True):
            carat = st.number_input("Carat", min_value=0.2, max_value=5.01, format="%.2f")
            cut = st.selectbox("Quality",["Fair", "Good", "Very Good", "Premium", "Ideal"], index=None, placeholder='Quality Cut type...')
            color = st.selectbox("Color", ["J", "I", "H", "G", "F", "E", "D"], index=None, placeholder='Color of Diamond...')
            clarity = st.selectbox("Cleaness", ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"], index=None, placeholder='Cleaness type...')
            
            col_d, col_t = st.columns(2)
            with col_d:
                depth = st.number_input("Depth (%)", min_value=43.0, max_value=79.0, format="%.2f")
            with col_t:
                table = st.number_input("Table", min_value=43.0, max_value=95.0, format="%.2f")
            
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                x = st.number_input("X", min_value=0.1, max_value=10.74, format="%.2f")
            with col_y:
                y = st.number_input("Y", min_value=0.1, max_value=58.9, format="%.2f")
            with col_z:
                z = st.number_input("Z", min_value=0.1, max_value=31.8, format="%.2f")
            submitted = st.form_submit_button('Predict')
            
            if submitted:
                if not carat: 
                    st.warning('Please fill the Gender field !!')
                elif not cut: 
                    st.warning('Please fill the Ethnicity field !!')
                elif not color: 
                    st.warning('Please fill the Parent Education field !!')
                elif not clarity: 
                    st.warning('Please fill the Lunch Type field !!')
                elif not depth: 
                    st.warning('Please fill the Test Course field !!')
                elif not table: 
                        st.warning('Please fill the roll number field !!')
                elif not x or not y or not z: 
                        st.warning('Please fill the roll number field !!')
                else:
                    # Convert data into dataframe
                    data = CustomDataPrice(carat, cut, color, clarity, depth, table, x, y, z)
                    
                    predict_df = data.get_data_price()
                    
                    # get a predict pipeline
                    predict_pipeline = PredictPipeline()
                    
                    # predict the result
                    result = predict_pipeline.predict_price(predict_df)
                    results = round(result[0], 2)
                    
                    st.success(f'Based on your input, My prediction for your 💎 Price is around ${results:.2f}', icon="🔎")
        
    
    # Carat    
    with tab3:
        st.subheader("🔎Do the Price Prediction")
        st.caption("**I guest, you already know what :blue[type and size] of :gem: that you need!**")
        with st.form('Diamond Carat', clear_on_submit=True):
            cut = st.selectbox("Quality",["Fair", "Good", "Very Good", "Premium", "Ideal"], index=None, placeholder='Quality Cut type...')
            color = st.selectbox("Color", ["J", "I", "H", "G", "F", "E", "D"], index=None, placeholder='Color of Diamond...')
            clarity = st.selectbox("Cleaness", ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"], index=None, placeholder='Cleaness type...')
            
            col_d, col_t = st.columns(2)
            with col_d:
                depth = st.number_input("Depth (%)", min_value=43.0, max_value=79.0, format="%.2f")
            with col_t:
                table = st.number_input("Table", min_value=43.0, max_value=95.0, format="%.2f")
            
            price = st.number_input("Budget ($)", min_value=0, max_value=18800)
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                x = st.number_input("X", min_value=0.1, max_value=10.74, format="%.2f")
            with col_y:
                y = st.number_input("Y", min_value=0.1, max_value=58.9, format="%.2f")
            with col_z:
                z = st.number_input("Z", min_value=0.1, max_value=31.8, format="%.2f")
            submitted = st.form_submit_button('Predict')
            
            if submitted:
                if not price: 
                    st.warning('Please fill the Gender field !!')
                elif not cut: 
                    st.warning('Please fill the Ethnicity field !!')
                elif not color: 
                    st.warning('Please fill the Parent Education field !!')
                elif not clarity: 
                    st.warning('Please fill the Lunch Type field !!')
                elif not depth: 
                    st.warning('Please fill the Test Course field !!')
                elif not table: 
                        st.warning('Please fill the roll number field !!')
                elif not x or not y or not z: 
                        st.warning('Please fill the roll number field !!')
                else:
                    # Convert data into dataframe
                    data = CustomDataCarat(cut, color, clarity, depth, table, price, x, y, z)
                    
                    predict_df_carat = data.get_data_carat()
                    
                    # get a predict pipeline
                    pred_pipeline = PredictPipeline()
                    
                    # predict the result
                    result = pred_pipeline.predict_carat(predict_df_carat)
                    results = round(result[0], 3)
                    to_gram = results / 5
                    
                    st.info('📝 1 carat = 0.2 gr')
                    st.success(f'Based on your input, My prediction you will get 💎 for {results:.2f} carat or {to_gram:.2f} gram', icon="🔎")
        

if __name__ == '__main__': 
    main() 
    
    