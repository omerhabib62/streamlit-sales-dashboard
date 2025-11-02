import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP (This is the CS part) ---
# Set the page configuration
# This MUST be the first Streamlit command
st.set_page_config(
    page_title="Simple Sales Dashboard",
    page_icon="📊",
    layout="wide"  # "wide" layout makes it look like a real dashboard
)

# --- DATA LOADING AND CLEANING (This is the BA + CS part) ---

# Function to load data (with caching to make it fast)
@st.cache_data  # Caches the data so it doesn't reload on every interaction
def load_data(filepath):
    try:
        # Read the CSV file
        df = pd.read_csv(filepath)
        
        # --- Data Cleaning (A key BA skill) ---
        # Convert 'Order Date' to datetime objects for time-series analysis
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        # Ensure 'Sales' is a numeric type (it should be, but good to check)
        df['Sales'] = pd.to_numeric(df['Sales'])
        
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found. Please make sure it's in the same folder.")
        return None

# Load the data
df = load_data('sales_data.csv')

if df is not None:
    # --- PAGE TITLE ---
    st.title("📊 Simple Sales Dashboard")
    st.markdown("This is a portfolio project to demonstrate Streamlit, Pandas, and Plotly.")

    # --- KPI METRICS (The BA "Dashboard" part) ---
    st.header("Key Performance Indicators (KPIs)")
    
    # Calculate KPIs
    total_sales = int(df['Sales'].sum())
    total_orders = int(df['Order ID'].nunique())
    average_order_value = int(df['Sales'].mean())
    
    # Display KPIs in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales (PKR)", f"{total_sales:,}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Average Order Value (PKR)", f"{average_order_value:,}")

    st.markdown("---") # Adds a horizontal line

    # --- CHARTS (The BA "Visualization" part) ---
    st.header("Sales Visualizations")

    # Group data for charts
    sales_over_time = df.groupby('Order Date')['Sales'].sum().reset_index()
    sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()

    # Create two columns for the charts
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        st.subheader("Sales Over Time")
        # Create an interactive line chart with Plotly
        fig_time = px.line(
            sales_over_time, 
            x='Order Date', 
            y='Sales', 
            title="Daily Sales Trend"
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with fig_col2:
        st.subheader("Sales by Category")
        # Create an interactive bar chart with Plotly
        fig_category = px.bar(
            sales_by_category, 
            x='Category', 
            y='Sales', 
            title="Total Sales per Category",
            color='Category' # Adds color
        )
        st.plotly_chart(fig_category, use_container_width=True)

    # --- RAW DATA (The "Transparency" part) ---
    st.header("Raw Data Table")
    st.markdown("View the raw data used for this dashboard.")
    # Display the dataframe as an interactive table
    st.dataframe(df.sort_values(by="Order Date", ascending=False))
