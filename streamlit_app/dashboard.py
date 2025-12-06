import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.connector import connect

# Page config
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    h2 {
        color: #334155;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        margin-top: 30px;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMetric label {
        color: white !important;
        font-size: 14px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Connect to Snowflake
@st.cache_resource
def get_snowflake_connection():
    return connect(
        user=st.secrets["SNOWFLAKE_USER"],
        password=st.secrets["SNOWFLAKE_PASSWORD"],
        account=st.secrets["SNOWFLAKE_ACCOUNT"],
        warehouse='COMPUTE_WH',
        database='JOB_ANALYTICS',
        schema='ANALYTICS'
    )

# Load data
@st.cache_data
def load_data(query):
    conn = get_snowflake_connection()
    df = pd.read_sql(query, conn)
    return df

# Title
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>💼 Job Market Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; margin-bottom: 30px;'>Comprehensive analysis of 160+ unique job positions across multiple dimensions</p>", unsafe_allow_html=True)
# KPIs with gradient background
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Unique Jobs", "167")

with col2:
    avg_salary = load_data("SELECT AVG((SALARY_MIN + SALARY_MAX)/2) as avg FROM JOB_LISTINGS_CLEAN WHERE SALARY_MIN IS NOT NULL")
    st.metric("💰 Average Salary", f"${avg_salary['AVG'][0]:,.0f}")

with col3:
    top_city = load_data("SELECT CITY FROM JOB_LISTINGS_CLEAN GROUP BY CITY ORDER BY COUNT(*) DESC LIMIT 1")
    st.metric("🏙️ Top Hiring City", top_city['CITY'][0])

with col4:
    companies = load_data("SELECT COUNT(DISTINCT COMPANY) as count FROM JOB_LISTINGS_CLEAN")
    st.metric("🏢 Active Companies", f"{companies['COUNT'][0]:,}")

st.markdown("<br>", unsafe_allow_html=True)

# 1. TOP CITIES BY AVERAGE SALARY
st.markdown("## 🏆 Top 10 Cities by Average Salary")

salary_by_location = load_data("""
    SELECT 
        CITY, 
        AVG((SALARY_MIN + SALARY_MAX) / 2) as AVG_SALARY_MIDPOINT,
        COUNT(*) as JOB_COUNT
    FROM JOB_LISTINGS_CLEAN
    WHERE SALARY_MIN IS NOT NULL AND SALARY_MAX IS NOT NULL
    GROUP BY CITY
    ORDER BY AVG((SALARY_MIN + SALARY_MAX) / 2) DESC
    LIMIT 10
""")

# Reverse order so highest is at top
salary_by_location = salary_by_location.iloc[::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=salary_by_location['CITY'],
    x=salary_by_location['AVG_SALARY_MIDPOINT'],
    orientation='h',
    text=salary_by_location['AVG_SALARY_MIDPOINT'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(size=11, color='#1e293b', family='Arial Black'),
    marker=dict(
        color=salary_by_location['AVG_SALARY_MIDPOINT'],
        colorscale=[[0, '#bfdbfe'], [0.5, '#3b82f6'], [1, '#1e3a8a']],
        showscale=False,
        line=dict(color='white', width=2)
    ),
    hovertemplate='<b>%{y}</b><br>Average Salary: <b>$%{x:,.0f}</b><br>Total Jobs: <b>%{customdata}</b><extra></extra>',
    customdata=salary_by_location['JOB_COUNT']
))

fig.update_layout(
    height=500,
    xaxis_title="Average Salary (USD)",
    yaxis_title="",
    plot_bgcolor='#f8fafc',
    paper_bgcolor='white',
    font=dict(size=12, family='Arial', color='#334155'),
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. MOST IN-DEMAND SKILLS
st.markdown("## 🔥 Top 15 Most In-Demand Skills")

skills_demand = load_data("""
    SELECT SKILL_NAME, JOB_COUNT, AVG_SALARY
    FROM SKILLS_DEMAND
    ORDER BY JOB_COUNT DESC
    LIMIT 15
""")

# Reverse for display
skills_demand = skills_demand.iloc[::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=skills_demand['SKILL_NAME'],
    x=skills_demand['JOB_COUNT'],
    orientation='h',
    text=skills_demand['JOB_COUNT'],
    textposition='outside',
    textfont=dict(size=11, color='#1e293b', family='Arial Black'),
    marker=dict(
        color=skills_demand['JOB_COUNT'],
        colorscale=[[0, '#d1fae5'], [0.5, '#34d399'], [1, '#059669']],
        showscale=False,
        line=dict(color='white', width=2)
    ),
    hovertemplate='<b>%{y}</b><br>Job Postings: <b>%{x}</b><br>Avg Salary: <b>$%{customdata:,.0f}</b><extra></extra>',
    customdata=skills_demand['AVG_SALARY']
))

fig.update_layout(
    height=600,
    xaxis_title="Number of Job Postings",
    yaxis_title="",
    plot_bgcolor='#f8fafc',
    paper_bgcolor='white',
    font=dict(size=12, family='Arial', color='#334155'),
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. JOB TYPE & COMPANIES
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📋 Job Type Distribution")
    
    job_type_dist = load_data("""
        SELECT 
            CASE 
                WHEN UPPER(JOB_TYPE) LIKE '%REMOTE%' THEN 'Remote'
                WHEN UPPER(JOB_TYPE) LIKE '%FULL%TIME%' OR UPPER(JOB_TYPE) = 'FULL-TIME' THEN 'Full-time'
                WHEN UPPER(JOB_TYPE) LIKE '%PART%TIME%' OR UPPER(JOB_TYPE) = 'PART-TIME' THEN 'Part-time'
                WHEN UPPER(JOB_TYPE) LIKE '%CONTRACT%' THEN 'Contract'
                WHEN UPPER(JOB_TYPE) LIKE '%INTERN%' THEN 'Internship'
                ELSE 'Other'
            END as CLEAN_JOB_TYPE,
            COUNT(*) as JOB_COUNT
        FROM JOB_LISTINGS_CLEAN
        WHERE JOB_TYPE IS NOT NULL
        GROUP BY CLEAN_JOB_TYPE
        ORDER BY JOB_COUNT DESC
    """)
    
    # Filter out "Other"
    job_type_dist = job_type_dist[job_type_dist['CLEAN_JOB_TYPE'] != 'Other']
    
    # Professional color palette
    colors_pie = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe']
    
    fig = go.Figure(data=[go.Pie(
        labels=job_type_dist['CLEAN_JOB_TYPE'],
        values=job_type_dist['JOB_COUNT'],
        hole=0.5,
        marker=dict(
            colors=colors_pie,
            line=dict(color='white', width=3)
        ),
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(size=12, family='Arial', color='#334155'),
        hovertemplate='<b>%{label}</b><br>Jobs: <b>%{value}</b><br>Percentage: <b>%{percent}</b><extra></extra>'
    )])
    
    fig.update_layout(
        height=450,
        showlegend=False,
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        annotations=[dict(
            text='Job<br>Types',
            x=0.5, y=0.5,
            font=dict(size=16, family='Arial Black', color='#334155'),
            showarrow=False
        )],
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("## 🏢 Top 10 Hiring Companies")
    
    top_companies = load_data("""
        SELECT COMPANY, TOTAL_POSITIONS, AVG_SALARY
        FROM COMPANY_INSIGHTS
        ORDER BY TOTAL_POSITIONS DESC
        LIMIT 10
    """)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top_companies['COMPANY'],
        y=top_companies['TOTAL_POSITIONS'],
        text=top_companies['TOTAL_POSITIONS'],
        textposition='outside',
        textfont=dict(size=11, color='#1e293b', family='Arial Black'),
        marker=dict(
            color=top_companies['TOTAL_POSITIONS'],
            colorscale=[[0, '#fef3c7'], [0.5, '#fbbf24'], [1, '#d97706']],
            showscale=False,
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>Open Positions: <b>%{y}</b><br>Avg Salary: <b>$%{customdata:,.0f}</b><extra></extra>',
        customdata=top_companies['AVG_SALARY']
    ))
    
    fig.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Open Positions",
        xaxis_tickangle=-45,
        plot_bgcolor='#f8fafc',
        paper_bgcolor='white',
        font=dict(size=11, family='Arial', color='#334155'),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. EXPERIENCE VS SALARY
st.markdown("## 📈 Salary Progression by Experience Level")

exp_salary_grouped = load_data("""
    SELECT 
        CASE 
            WHEN EXPERIENCE_REQUIRED < 2 THEN '0-2 years'
            WHEN EXPERIENCE_REQUIRED < 5 THEN '2-5 years'
            WHEN EXPERIENCE_REQUIRED < 8 THEN '5-8 years'
            ELSE '8+ years'
        END as EXPERIENCE_LEVEL,
        AVG((SALARY_MIN + SALARY_MAX) / 2) as AVG_SALARY,
        COUNT(*) as JOB_COUNT,
        MIN((SALARY_MIN + SALARY_MAX) / 2) as MIN_SALARY,
        MAX((SALARY_MIN + SALARY_MAX) / 2) as MAX_SALARY
    FROM JOB_LISTINGS_CLEAN
    WHERE EXPERIENCE_REQUIRED IS NOT NULL 
    AND SALARY_MIN IS NOT NULL 
    AND SALARY_MAX IS NOT NULL
    GROUP BY EXPERIENCE_LEVEL
    ORDER BY 
        CASE EXPERIENCE_LEVEL
            WHEN '0-2 years' THEN 1
            WHEN '2-5 years' THEN 2
            WHEN '5-8 years' THEN 3
            WHEN '8+ years' THEN 4
        END
""")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=exp_salary_grouped['EXPERIENCE_LEVEL'],
    y=exp_salary_grouped['AVG_SALARY'],
    text=exp_salary_grouped['AVG_SALARY'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='#1e293b', family='Arial Black'),
    marker=dict(
        color=exp_salary_grouped['AVG_SALARY'],
        colorscale=[[0, '#e9d5ff'], [0.5, '#a78bfa'], [1, '#6d28d9']],
        showscale=False,
        line=dict(color='white', width=2)
    ),
    hovertemplate='<b>%{x}</b><br>Average Salary: <b>$%{y:,.0f}</b><br>Job Count: <b>%{customdata}</b><extra></extra>',
    customdata=exp_salary_grouped['JOB_COUNT']
))

fig.update_layout(
    height=500,
    xaxis_title="Experience Level",
    yaxis_title="Average Salary (USD)",
    plot_bgcolor='#f8fafc',
    paper_bgcolor='white',
    font=dict(size=12, family='Arial', color='#334155'),
    showlegend=False,
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False)
)

st.plotly_chart(fig, use_container_width=True)

# Professional insights cards
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

salary_increase = exp_salary_grouped[exp_salary_grouped['EXPERIENCE_LEVEL'] == '8+ years']['AVG_SALARY'].values[0] - \
                 exp_salary_grouped[exp_salary_grouped['EXPERIENCE_LEVEL'] == '0-2 years']['AVG_SALARY'].values[0]

with col1:
    st.info(f"**💡 Entry Level (0-2 years)**\n\nAverage Salary: **${exp_salary_grouped[exp_salary_grouped['EXPERIENCE_LEVEL'] == '0-2 years']['AVG_SALARY'].values[0]:,.0f}**")
with col2:
    st.success(f"**📊 Mid-Level (2-5 years)**\n\nAverage Salary: **${exp_salary_grouped[exp_salary_grouped['EXPERIENCE_LEVEL'] == '2-5 years']['AVG_SALARY'].values[0]:,.0f}**")
with col3:
    st.warning(f"**🎯 Senior (8+ years)**\n\nAverage Salary: **${exp_salary_grouped[exp_salary_grouped['EXPERIENCE_LEVEL'] == '8+ years']['AVG_SALARY'].values[0]:,.0f}**\n\n*+${salary_increase:,.0f} vs Entry*")

# Professional Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
        <h3 style='color: white; margin: 0;'>📊 Data Pipeline Architecture</h3>
        <p style='margin: 10px 0 5px 0; font-size: 14px;'><b>Technology Stack:</b> Streamlit • Snowflake • Apache Airflow • Docker • Python</p>
        <p style='margin: 5px 0; font-size: 13px;'>Data Source: 160+ unique job positions | Last Updated: 2025-12-06 | Pipeline Status: ✅ Active</p>
        <p style='margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;'>Automated daily refresh at 00:00 UTC via Apache Airflow orchestration</p>
    </div>
""", unsafe_allow_html=True)
