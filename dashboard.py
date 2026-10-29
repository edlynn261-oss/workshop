import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='NYC Yellow Taxi | Capstone Dashboard', page_icon='🚕', layout='wide')
st.title('🚕 NYC Yellow Taxi — Capstone Dashboard')
st.caption('January–March 2024 · Cleaned taxi trip data · DuckDB + dbt')
DB = Path(__file__).resolve().parent / 'warehouse' / 'taxi.duckdb'
if not DB.exists():
    st.error(f'Database not found: {DB}. Run the dbt models and check the database location.')
    st.stop()

@st.cache_data

def query(sql):
    with duckdb.connect(str(DB), read_only=True) as con:
        return con.execute(sql).df()

try:
    monthly = query('SELECT * FROM trips_by_month ORDER BY pickup_month')
    zones = query('SELECT * FROM pickup_zone_analysis')
    time = query('SELECT * FROM pickup_time_analysis')
    tips = query('SELECT * FROM payment_tipping_analysis')
    airport = query('SELECT * FROM airport_trip_analysis')
except Exception as e:
    st.error(f'Unable to read a model: {e}')
    st.info('Run: dbt run --select trips_by_month pickup_zone_analysis pickup_time_analysis payment_tipping_analysis airport_trip_analysis')
    st.stop()

months = monthly['pickup_month'].astype(str).tolist()
all_trips = int(monthly['trips'].sum())
all_revenue = float(monthly['revenue'].sum())
c1,c2,c3,c4=st.columns(4)
c1.metric('Total trips', f'{all_trips:,}')
c2.metric('Total revenue', f'${all_revenue/1e6:,.2f}M')
c3.metric('Busiest pickup zone', str(zones.sort_values('total_trips',ascending=False).iloc[0]['zone_name']))
c4.metric('Peak hour', f"{int(time.groupby('pickup_hour')['total_trips'].sum().idxmax()):02d}:00")
st.info('All metrics use the cleaned January–March dataset. This dashboard displays pre-aggregated dbt models; its charts are not dynamically filtered by month.')

tabs=st.tabs(['Monthly trends','Pickup zones','Hours & weekdays','Tipping','Airport trips'])
with tabs[0]:
    st.subheader('Question 1 · Monthly trips and revenue')
    a,b=st.columns(2)
    with a: st.plotly_chart(px.bar(monthly,x='pickup_month',y='trips',title='Trips by month',labels={'pickup_month':'Month','trips':'Trips'}),use_container_width=True)
    with b: st.plotly_chart(px.line(monthly,x='pickup_month',y='revenue',markers=True,title='Revenue by month',labels={'pickup_month':'Month','revenue':'Revenue (USD)'}),use_container_width=True)
    st.dataframe(monthly,use_container_width=True,hide_index=True)
with tabs[1]:
    st.subheader('Question 2 · Busiest pickup zones and borough revenue')
    n=st.slider('Number of pickup zones',5,25,10)
    top=zones.nlargest(n,'total_trips').sort_values('total_trips')
    st.plotly_chart(px.bar(top,x='total_trips',y='zone_name',orientation='h',color='borough',title=f'Top {n} pickup zones',labels={'total_trips':'Trips','zone_name':'Pickup zone'}),use_container_width=True)
    borough=zones.groupby('borough',as_index=False)[['total_trips','total_revenue']].sum().sort_values('total_revenue',ascending=False)
    st.plotly_chart(px.bar(borough,x='borough',y='total_revenue',title='Revenue by pickup borough',labels={'total_revenue':'Revenue (USD)','borough':'Borough'}),use_container_width=True)
    st.caption('Unknown, N/A and EWR are lookup categories, not NYC boroughs.')
with tabs[2]:
    st.subheader('Question 3 · Peak pickup times')
    hourly=time.groupby('pickup_hour',as_index=False)['total_trips'].sum().sort_values('pickup_hour')
    daily=time.groupby(['day_number','pickup_day'],as_index=False)['total_trips'].sum().sort_values('day_number')
    a,b=st.columns(2)
    with a: st.plotly_chart(px.bar(hourly,x='pickup_hour',y='total_trips',title='Trips by hour',labels={'pickup_hour':'Hour (24-hour)','total_trips':'Trips'}),use_container_width=True)
    with b: st.plotly_chart(px.bar(daily,x='pickup_day',y='total_trips',title='Trips by weekday',labels={'pickup_day':'Day','total_trips':'Trips'}),use_container_width=True)
    st.caption('Weekday totals are not adjusted for the number of occurrences of each weekday.')
with tabs[3]:
    st.subheader('Question 4 · Recorded tipping by payment type')
    a,b=st.columns(2)
    with a: st.plotly_chart(px.bar(tips,x='payment_type',y='avg_tip',title='Average recorded tip',labels={'payment_type':'Payment type','avg_tip':'Tip (USD)'}),use_container_width=True)
    with b: st.plotly_chart(px.bar(tips,x='payment_type',y='tipping_rate',title='Trips with positive recorded tip',labels={'payment_type':'Payment type','tipping_rate':'Trips (%)'}),use_container_width=True)
    st.warning('NYC TLC tip_amount excludes cash tips. A near-zero cash tipping rate does not mean cash passengers never tip.')
    st.dataframe(tips,use_container_width=True,hide_index=True)
with tabs[4]:
    st.subheader('Question 5 · Airport vs non-airport trips')
    st.caption('Airport trips start or end at JFK (132), LaGuardia (138), or Newark (1).')
    metrics=[('trip_share_pct','Share of trips','%'),('revenue_share_pct','Share of revenue','%'),('avg_fare','Average fare','USD'),('avg_duration_minutes','Average duration','minutes')]
    for row in range(2):
        cols=st.columns(2)
        for col,(field,title,unit) in zip(cols,metrics[row*2:row*2+2]):
            with col:
                fig=px.bar(airport,x='trip_type',y=field,color='trip_type',text_auto='.2f',title=title,labels={'trip_type':'Trip type',field:unit},color_discrete_map={'Airport':'#2563eb','Non-Airport':'#f59e0b'})
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
    st.dataframe(airport,use_container_width=True,hide_index=True)
    st.success('Airport trips represent a small share of trips but a disproportionately large share of revenue.')
