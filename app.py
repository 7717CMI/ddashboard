import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the load postings data"""
    try:
        with open('nextload.json', 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data['load_postings'])
        
        # Convert timestamps to datetime
        df['posted_date'] = pd.to_datetime(df['postedTimestamp'], unit='ms')
        df['pickup_date'] = pd.to_datetime(df['pickupTimestamp'], unit='ms')
        
        # Convert rate from cents to dollars
        df['rate_dollars'] = df['rateCents'] / 100
        df['rate_per_mile_dollars'] = df['rateCentsPerMile'] / 100
        
        # Create origin-destination pairs
        df['route'] = df['originCity'] + ', ' + df['originState'] + ' → ' + df['destinationCity'] + ', ' + df['destinationState']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    # Header
    st.markdown('<h1 class="main-header">🚛 Logistics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("No data available. Please check the data file.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Equipment type filter
    equipment_types = ['All'] + sorted(df['equipmentType'].unique().tolist())
    selected_equipment = st.sidebar.selectbox("Equipment Type", equipment_types)
    
    # State filter
    all_states = sorted(set(df['originState'].tolist() + df['destinationState'].tolist()))
    selected_state = st.sidebar.selectbox("State", ['All'] + all_states)
    
    # Company filter
    companies = ['All'] + sorted(df['companyName'].unique().tolist())
    selected_company = st.sidebar.selectbox("Company", companies)
    
    # Rate range filter
    min_rate = float(df['rate_dollars'].min())
    max_rate = float(df['rate_dollars'].max())
    rate_range = st.sidebar.slider("Rate Range ($)", min_rate, max_rate, (min_rate, max_rate))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_equipment != 'All':
        filtered_df = filtered_df[filtered_df['equipmentType'] == selected_equipment]
    
    if selected_state != 'All':
        filtered_df = filtered_df[
            (filtered_df['originState'] == selected_state) | 
            (filtered_df['destinationState'] == selected_state)
        ]
    
    if selected_company != 'All':
        filtered_df = filtered_df[filtered_df['companyName'] == selected_company]
    
    filtered_df = filtered_df[
        (filtered_df['rate_dollars'] >= rate_range[0]) & 
        (filtered_df['rate_dollars'] <= rate_range[1])
    ]
    
    # Key metrics
    st.header("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Loads",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):+,}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        avg_rate = filtered_df['rate_dollars'].mean()
        st.metric(
            label="Average Rate",
            value=f"${avg_rate:,.0f}",
            delta=f"${avg_rate - df['rate_dollars'].mean():+,.0f}" if len(filtered_df) != len(df) else None
        )
    
    with col3:
        total_distance = filtered_df['distanceMiles'].sum()
        st.metric(
            label="Total Distance",
            value=f"{total_distance:,} miles",
            delta=f"{total_distance - df['distanceMiles'].sum():+,} miles" if len(filtered_df) != len(df) else None
        )
    
    with col4:
        unique_companies = filtered_df['companyName'].nunique()
        st.metric(
            label="Companies",
            value=f"{unique_companies}",
            delta=f"{unique_companies - df['companyName'].nunique():+}" if len(filtered_df) != len(df) else None
        )
    
    st.markdown("---")
    
    # Charts section
    st.header("📈 Analytics")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Geographic Analysis", 
        "💰 Rate Analysis", 
        "🚛 Equipment Analysis", 
        "🏢 Company Analysis",
        "📅 Time Analysis"
    ])
    
    with tab1:
        st.subheader("Load Distribution Map")
        
        # Create scatter mapbox for origins and destinations
        fig_map = go.Figure()
        
        # Add origin points
        fig_map.add_trace(go.Scattermapbox(
            lat=filtered_df['originLatitude'],
            lon=filtered_df['originLongitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='red',
                opacity=0.7
            ),
            text=filtered_df['originCity'] + ', ' + filtered_df['originState'],
            name='Origins',
            hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
        ))
        
        # Add destination points
        fig_map.add_trace(go.Scattermapbox(
            lat=filtered_df['destinationLatitude'],
            lon=filtered_df['destinationLongitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='blue',
                opacity=0.7
            ),
            text=filtered_df['destinationCity'] + ', ' + filtered_df['destinationState'],
            name='Destinations',
            hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
        ))
        
        fig_map.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=39.8283, lon=-98.5795),  # Center of USA
                zoom=3
            ),
            height=600,
            title="Load Origins (Red) and Destinations (Blue)"
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Top routes
        st.subheader("Top Routes")
        route_counts = filtered_df['route'].value_counts().head(10)
        
        fig_routes = px.bar(
            x=route_counts.values,
            y=route_counts.index,
            orientation='h',
            title="Most Popular Routes",
            labels={'x': 'Number of Loads', 'y': 'Route'}
        )
        fig_routes.update_layout(height=400)
        st.plotly_chart(fig_routes, use_container_width=True)
    
    with tab2:
        st.subheader("Rate Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rate histogram
            fig_hist = px.histogram(
                filtered_df,
                x='rate_dollars',
                nbins=50,
                title="Rate Distribution",
                labels={'rate_dollars': 'Rate ($)', 'count': 'Number of Loads'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Rate per mile histogram
            fig_hist_mile = px.histogram(
                filtered_df,
                x='rate_per_mile_dollars',
                nbins=50,
                title="Rate per Mile Distribution",
                labels={'rate_per_mile_dollars': 'Rate per Mile ($)', 'count': 'Number of Loads'}
            )
            st.plotly_chart(fig_hist_mile, use_container_width=True)
        
        # Rate vs Distance scatter
        st.subheader("Rate vs Distance Analysis")
        fig_scatter = px.scatter(
            filtered_df,
            x='distanceMiles',
            y='rate_dollars',
            color='equipmentType',
            size='weight',
            hover_data=['originCity', 'destinationCity', 'companyName'],
            title="Rate vs Distance by Equipment Type",
            labels={'distanceMiles': 'Distance (miles)', 'rate_dollars': 'Rate ($)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab3:
        st.subheader("Equipment Type Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Equipment type pie chart
            equipment_counts = filtered_df['equipmentType'].value_counts()
            fig_pie = px.pie(
                values=equipment_counts.values,
                names=equipment_counts.index,
                title="Load Distribution by Equipment Type"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Average rate by equipment type
            avg_rates = filtered_df.groupby('equipmentType')['rate_dollars'].mean().sort_values(ascending=True)
            fig_bar = px.bar(
                x=avg_rates.values,
                y=avg_rates.index,
                orientation='h',
                title="Average Rate by Equipment Type",
                labels={'x': 'Average Rate ($)', 'y': 'Equipment Type'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Weight distribution by equipment type
        st.subheader("Weight Distribution by Equipment Type")
        fig_box = px.box(
            filtered_df,
            x='equipmentType',
            y='weight',
            title="Weight Distribution by Equipment Type",
            labels={'weight': 'Weight (lbs)', 'equipmentType': 'Equipment Type'}
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab4:
        st.subheader("Company Analysis")
        
        # Top companies by load count
        company_counts = filtered_df['companyName'].value_counts().head(15)
        fig_companies = px.bar(
            x=company_counts.values,
            y=company_counts.index,
            orientation='h',
            title="Top Companies by Load Count",
            labels={'x': 'Number of Loads', 'y': 'Company'}
        )
        fig_companies.update_layout(height=500)
        st.plotly_chart(fig_companies, use_container_width=True)
        
        # Company performance metrics
        st.subheader("Company Performance Metrics")
        company_metrics = filtered_df.groupby('companyName').agg({
            'rate_dollars': ['mean', 'count'],
            'distanceMiles': 'mean',
            'weight': 'mean'
        }).round(2)
        
        company_metrics.columns = ['Avg_Rate', 'Load_Count', 'Avg_Distance', 'Avg_Weight']
        company_metrics = company_metrics.sort_values('Load_Count', ascending=False).head(10)
        
        st.dataframe(company_metrics, use_container_width=True)
    
    with tab5:
        st.subheader("Time-based Analysis")
        
        # Loads by posted date
        filtered_df['posted_date_only'] = filtered_df['posted_date'].dt.date
        daily_counts = filtered_df.groupby('posted_date_only').size().reset_index()
        daily_counts.columns = ['Date', 'Load_Count']
        
        fig_timeline = px.line(
            daily_counts,
            x='Date',
            y='Load_Count',
            title="Load Postings Over Time",
            labels={'Load_Count': 'Number of Loads', 'Date': 'Date'}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Pickup date analysis
        filtered_df['pickup_date_only'] = filtered_df['pickup_date'].dt.date
        pickup_counts = filtered_df.groupby('pickup_date_only').size().reset_index()
        pickup_counts.columns = ['Date', 'Pickup_Count']
        
        fig_pickup = px.line(
            pickup_counts,
            x='Date',
            y='Pickup_Count',
            title="Scheduled Pickups Over Time",
            labels={'Pickup_Count': 'Number of Pickups', 'Date': 'Date'}
        )
        st.plotly_chart(fig_pickup, use_container_width=True)
    
    # Data table
    st.markdown("---")
    st.header("📋 Data Table")
    
    # Show filtered data
    display_columns = [
        'referenceNumber', 'route', 'equipmentType', 'rate_dollars', 
        'distanceMiles', 'weight', 'companyName', 'posted_date'
    ]
    
    st.dataframe(
        filtered_df[display_columns].rename(columns={
            'referenceNumber': 'Reference #',
            'route': 'Route',
            'equipmentType': 'Equipment',
            'rate_dollars': 'Rate ($)',
            'distanceMiles': 'Distance (miles)',
            'weight': 'Weight (lbs)',
            'companyName': 'Company',
            'posted_date': 'Posted Date'
        }),
        use_container_width=True,
        height=400
    )

if __name__ == "__main__":
    main()
