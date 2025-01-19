class Config:
    # Streamlit configs
    PAGE_TITLE = "Data Visualization Dashboard"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    
    # Visualization settings
    DEFAULT_PLOT_HEIGHT = 500
    MAX_DISPLAY_ROWS = 1000
    CHART_THEME = "plotly"
    
    # Gemini API settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    MODEL_NAME = "gemini-pro"