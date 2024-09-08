import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


dataset = pd.read_csv('data/diamonds.csv')
do_cut = ['Ideal', 'Premium', 'Very Good', 'Good', 'Fair']
do_color = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
do_clarity = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1']

def cut_distribution():
    data_cut = dataset['cut'].value_counts().reindex(do_cut)
    df = pd.DataFrame({'Cut': data_cut.index, 'Total': data_cut.values})
    
    fig = px.bar(df, x="Cut", y="Total", height=320, width=400)
    st.plotly_chart(fig)
    
    
def color_distribution():
    data_color = dataset['color'].value_counts().reindex(do_color)
    df = pd.DataFrame({'Color': data_color.index, 'Total': data_color.values})
    
    fig = px.bar(df, x="Color", y="Total", height=320, width=400)
    st.plotly_chart(fig)
    
    
def clarity_distribution():
    data_clarity = dataset['clarity'].value_counts().reindex(do_clarity)
    df = pd.DataFrame({'Clarity': data_clarity.index, 'Total': data_clarity.values})
    
    fig = px.bar(df, x="Clarity", y="Total", height=320, width=400)
    st.plotly_chart(fig)
    
 
def show_clarity(clarity, container):
    col1, col2 = container.columns(2)
    if clarity=="I1":
        with col1:
            st.write("**Inclusion 1 (I1)**")
            st.write("Included (1st Degree) – I1 clarity inclusions are even more obvious and clearly seen than SI2 clarity inclusions. Most I1 inclusions are visible to the naked eye—even on brilliant cuts.")
        with col2:
            st.image("image/i1.png", caption="Inclusion 1", width=280)
    elif clarity=="SI2":
        with col1:
            st.write("**Small Inclusions 2 (SI2)**")
            st.write("Slightly Included (2nd Degree) – SI2 clarity inclusions are seen clearly and obviously with the help of a jeweler’s loupe. With step cuts like Emerald and Asscher cuts, an SI2 clarity inclusion will most likely be visible to the naked eye.")
        with col2:
            st.image("image/si2.png", caption="Small Inclusions 2", width=280)
    elif clarity=="SI1":
        with col1:
            st.write("**Small Inclusions 1 (SI1)**")
            st.write("Slightly Included (1st Degree) – SI1 Clarity inclusions are easily found with a standard jeweler’s loupe at 10x magnification. With most shapes, SI1 clarity inclusions are almost always clean to the naked eye.")
        with col2:
            st.image("image/si1.png", caption="Small Inclusions 1", width=280)
    elif clarity=="VS2":
        with col1:
            st.write("**Very Small Inclusions 2 (VS2)**")
            st.write("Very Slightly Included (2nd Degree) – VS2 clarity inclusions are almost always easily noticeable at 10x magnification (standard jeweler’s loupe). Occasionally, the inclusion will be located in a difficult-to-spot location, but otherwise, the inclusion is large enough that it can be spotted quickly under magnification.")
        with col2:
            st.image("image/vs2.png", caption="Very Small Inclusions 2", width=280)
    elif clarity=="VS1":
        with col1:
            st.write("**Very Small Inclusion 1 (VS1)**")
            st.write("Very Slightly Included (1st Degree) – VS1 diamond clarity inclusions are just barely visible under 10x magnification (standard jeweler’s loupe). When looking for VS1 clarity inclusions with a loupe, it can sometimes take a good few seconds until the pinpoint is located.")
        with col2:
            st.image("image/vs1.png", caption="Very Small Inclusion 1", width=280)
    elif clarity=="VVS2":
        with col1:
            st.write("**Very Very Small Inclusions 2 (VVS2)**")
            st.write("Very Very Slightly Included (2nd Degree) – Diamond clarity inclusions rated VVS2 are sometimes just barely visible under 10x magnification (standard jeweler’s loupe). When they are visible, they are quite difficult to find and can often take quite a while to locate")
        with col2:
            st.image("image/vvs2.png", caption="Very Very Small Inclusions 2", width=280)
    elif clarity=="VVS1":
        with col1:
            st.write("**Very Very Small Inclusions 1 (VVS1)**")
            st.write("Very Very Slightly Included (1st Degree) – Diamond clarity inclusions rated VVS1 are not visible at all under 10x magnification.")
        with col2:
            st.image("image/vvs1.png", caption="Very Very Small Inclusion 1", width=280)
    else:
        with col1:
            st.write("**Internal Flawless**")
            st.write("Internally Flawless / Flawless – No internal or external imperfections. Flawless diamonds are extremely rare.")
        with col2:
            st.image("image/IF.png", caption="Internal Flawless", width=280)

    
def average_price():
    container = st.container()
    mean_cut = dataset.groupby('cut')['price'].mean().reindex(do_cut)
    mean_color = dataset.groupby('color')['price'].mean().reindex(do_color)
    mean_clarity = dataset.groupby('clarity')['price'].mean().reindex(do_clarity)
    
    mean_cut = pd.DataFrame({'cut': mean_cut.index, 'price': mean_cut.values})
    mean_color = pd.DataFrame({'color': mean_color.index, 'price': mean_color.values})
    mean_clarity = pd.DataFrame({'clarity': mean_clarity.index, 'price': mean_clarity.values})

    # Create the bar charts
    trace1 = go.Bar(
        x=mean_cut['cut'],
        y=round(mean_cut['price'], 2),
        name="Cut",
        marker=dict(color='skyblue')
    )
    trace2 = go.Bar(
        x=mean_color['color'],
        y=round(mean_color['price'], 2),
        name="Color",
        marker=dict(color='lightgreen')
    )
    trace3 = go.Bar(
        x=mean_clarity['clarity'],
        y=round(mean_clarity['price'], 2),
        name="Clarity",
        marker=dict(color='salmon')
    )
    
    
    # Layout with vertical alignment (1 column, 3 rows)
    layout = go.Layout(
        title='💰📊 Average Price by Cut, Color, and Clarity',
        xaxis=dict(title='Cut'),  # For Cut
        yaxis=dict(title='Average Price', domain=[0, 1]),
        xaxis2=dict(title='Color'),  # For Color
        yaxis2=dict(title='Average Price', anchor='x2'),
        xaxis3=dict(title='Clarity'),  # For Clarity
        yaxis3=dict(title='Average Price', anchor='x3'),
        height=480,

        grid=dict(rows=3, columns=1, pattern='independent'),  # 3 rows, 1 column
    )

    # Combine traces and create the figure
    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    
    container.plotly_chart(fig)
    container.markdown("""
    - In the `'cut'` feature, the average prices tend to be similar. _The highest grade, namely the **Ideal** grade, has the lowest average price among the other grades_.
    - In the `'color'` feature, *the lower the color grade, the higher the price of diamonds*.
    - In the `'clarity'` feature, *diamonds with a lower grade have a higher average price*.
    """)


def price_distribution():
    container = st.container()
    trace1 = go.Histogram(
        x=dataset['price'],
        opacity=0.75)

    layout = go.Layout(barmode='overlay',
                    title='💲 Diamond Price Distribution',
                    xaxis=dict(title='Diamond Price'),
                    yaxis=dict(title='Count'),
                    height=480
    )

    fig = go.Figure(data=[trace1], layout=layout)
    container.plotly_chart(fig)
    container.markdown('📓 **The higher the price of diamonds, the fewer there are available, and vice versa. Also, people tend to buy at the average price.**')
    
    
