import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from config import Config
from utils import load_data, get_numeric_columns, get_categorical_columns
from components import render_sidebar, render_data_stats, render_visualization_options, render_ai_insights
from error_handler import handle_errors

# Configure page settings
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT
)

@handle_errors
def main():
    st.title("📊 Data Visualization Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", 
                                   type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        # Load and cache data
        df = load_data(uploaded_file)
        
        if df is not None:
            # Store dataframe in session state
            st.session_state['df'] = df
            
            # Display basic data statistics
            render_data_stats(df)
            
            # AI Insights
            render_ai_insights(df)
            
            # Sidebar controls
            render_sidebar(df)
            
            # Main visualization area
            st.header("📈 Visualizations")
            
            # Visualization options
            viz_type = render_visualization_options()
            
            # Generate visualizations based on selection
            if viz_type == "Scatter Plot":
                x_col = st.selectbox("X-axis", get_numeric_columns(df))
                y_col = st.selectbox("Y-axis", get_numeric_columns(df))
                color_col = st.selectbox("Color by", ["None"] + get_categorical_columns(df))
                
                fig = px.scatter(df, x=x_col, y=y_col, 
                               color=None if color_col == "None" else color_col,
                               title=f"Scatter Plot: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Line Chart":
                x_col = st.selectbox("X-axis", get_numeric_columns(df))
                y_col = st.selectbox("Y-axis", get_numeric_columns(df))
                
                fig = px.line(df, x=x_col, y=y_col,
                            title=f"Line Chart: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Bar Chart":
                x_col = st.selectbox("X-axis", get_categorical_columns(df))
                y_col = st.selectbox("Y-axis", get_numeric_columns(df))
                
                fig = px.bar(df, x=x_col, y=y_col,
                           title=f"Bar Chart: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Histogram":
                col = st.selectbox("Column", get_numeric_columns(df))
                bins = st.slider("Number of bins", 5, 100, 30)
                
                fig = px.histogram(df, x=col, nbins=bins,
                                title=f"Histogram of {col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Box Plot":
                y_col = st.selectbox("Values", get_numeric_columns(df))
                x_col = st.selectbox("Categories", ["None"] + get_categorical_columns(df))
                
                if x_col == "None":
                    fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
                else:
                    fig = px.box(df, x=x_col, y=y_col, 
                               title=f"Box Plot of {y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Correlation Matrix":
                numeric_df = df.select_dtypes(include=['int64', 'float64'])
                
                if not numeric_df.empty:
                    fig = px.imshow(numeric_df.corr(),
                                  title="Correlation Matrix",
                                  color_continuous_scale="RdBu")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns available for correlation matrix")
            
            # Data table view
            if st.checkbox("Show Data Table"):
                st.dataframe(df)

if __name__ == "__main__":
    main()