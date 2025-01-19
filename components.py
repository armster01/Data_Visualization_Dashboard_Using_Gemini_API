import streamlit as st
import pandas as pd

def render_sidebar(df):
    """Render the sidebar with data filters and controls"""
    with st.sidebar:
        st.title("🎛️ Controls")
        
        # Data filtering
        st.header("Data Filters")
        
        # Numeric filters
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            step = (max_val - min_val) / 100
            
            values = st.slider(
                f"Filter {col}",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                step=step
            )
            df = df[df[col].between(values[0], values[1])]
        
        # Categorical filters
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            options = ['All'] + list(df[col].unique())
            selection = st.multiselect(f"Filter {col}", options, ['All'])
            if 'All' not in selection:
                df = df[df[col].isin(selection)]
        
        st.session_state['filtered_df'] = df

def render_data_stats(df):
    """Display basic statistics about the dataset"""
    st.header("📊 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", df.isna().sum().sum())

def render_visualization_options():
    """Render visualization type selector"""
    viz_types = [
        "Scatter Plot",
        "Line Chart",
        "Bar Chart",
        "Histogram",
        "Box Plot",
        "Correlation Matrix"
    ]
    
    return st.selectbox("Select Visualization Type", viz_types)

def render_ai_insights(df):
    """Render AI-powered insights about the data"""
    st.header("🤖 AI Insights")
    
    if st.button("Generate Insights"):
        with st.spinner("Analyzing data..."):
            from utils import get_data_insights
            insights = get_data_insights(df)
            st.markdown(insights)