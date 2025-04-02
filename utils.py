import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def load_data(file):
    """Load and cache data from uploaded file"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def get_numeric_columns(df):
    """Get list of numeric columns from dataframe"""
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

def get_categorical_columns(df):
    """Get list of categorical columns from dataframe"""
    return df.select_dtypes(include=['object']).columns.tolist()

def format_number(num):
    """Format numbers for display"""
    if isinstance(num, (int, float)):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)
    return num

def get_data_insights(df):
    """Get AI-powered insights about the data using Gemini"""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
        
        # Prepare data summary
        data_info = f"""
        Dataset Summary:
        - Shape: {df.shape}
        - Columns: {', '.join(df.columns)}
        - Numeric columns: {', '.join(get_numeric_columns(df))}
        - Categorical columns: {', '.join(get_categorical_columns(df))}
        - Missing values: {df.isna().sum().sum()}
        
        Basic Statistics:
        {df.describe().to_string()}
        """
        
        prompt = f"""
        Analyze this dataset and provide key insights:
        {data_info}
        
        Please provide:
        1. Key observations about the data
        2. Potential patterns or trends
        3. Suggestions for visualization
        4. Data quality issues if any
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"
