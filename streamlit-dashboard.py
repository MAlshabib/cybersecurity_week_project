import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
# Configure Altair to use transparent backgrounds
alt.themes.enable('dark')
alt.data_transformers.disable_max_rows()

# Load dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("cybersecurity_dataset.csv")

df = load_data()

# 🎯 Flag Attacks with More Than 500K Users Affected and Long Resolution Time
df['Critical'] = False

for i, row in df.iterrows():
    if row['Number of Affected Users'] > 500000 and row['Incident Resolution Time (in Hours)'] > 48:
        df.at[i, 'Critical'] = True

# Add Severity column based on Financial Loss
df['Severity'] = df['Financial Loss (in Million $)'].apply(
    lambda loss: 'High' if loss > 70 else 'Medium' if loss > 40 else 'Low'
)

def classify_complexity(row):
    if row['Security Vulnerability Type'] in ['Zero-day', 'Unpatched Software']:
        return 'High'
    elif row['Security Vulnerability Type'] in ['Weak Passwords']:
        return 'Medium'
    else:
        return 'Low'

# Why: Assign a simple tag based on attack type and vulnerability.
# Insight: Helps distinguish between technically sophisticated vs. socially engineered attacks.
def classify_complexity(row):
    if row['Security Vulnerability Type'] in ['Zero-day', 'Unpatched Software']:
        return 'High'
    elif row['Security Vulnerability Type'] in ['Weak Passwords']:
        return 'Medium'
    else:
        return 'Low'

df['Attack Complexity'] = df.apply(classify_complexity, axis=1)

# Why: Combine defense mechanism and resolution time to evaluate response.
# Insight: Tells if defenses like VPN or Firewall are handling fast responses or not.
df['Defense Effectiveness'] = df['Incident Resolution Time (in Hours)'].apply(lambda x: 'Effective' if x <= 24 else 'Ineffective')

# Why: Categorize attacks by their entry vector (human vs. system).
# Insight: Supports prevention strategy design.
human_vectors = ['Social Engineering', 'Weak Passwords'] # can add more
df['Attack Vector Type'] = df['Security Vulnerability Type'].apply(
    lambda x: 'Human' if x in human_vectors else 'System'
)

# Page config
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

# Custom CSS for modern dark styling
st.markdown("""
<style>
    /* Hide Streamlit top menu and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .st-emotion-cache-zq5wmm.ezrtsby0 {display: none;}

    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    .main .block-container { background: transparent; color: #e2e8f0; padding-top: 2rem; }
    .css-1d391kg { background: linear-gradient(180deg,#1e293b 0%,#334155 100%) !important; border-radius:0 25px 25px 0!important; border-right:1px solid #475569; }
    .main-header { font-size:3rem; font-weight:700; text-align:center;
        background: linear-gradient(135deg,#60a5fa 0%,#a78bfa 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .metric-card { background:linear-gradient(135deg,#1e40af 0%,#7c3aed 100%);
        padding:2rem; border-radius:20px; color:#fff; text-align:center;
        box-shadow:0 20px 40px -10px rgba(0,0,0,0.4);
        backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.1);
        transition:transform .3s ease; }
    .metric-card:hover { transform:translateY(-5px); }
    .metric-value { font-size:2.8rem; font-weight:700; margin-bottom:.5rem; }
    .metric-label { font-size:1.1rem; opacity:.9; font-weight:500; }
    /* Chart card styling… */
    .chart-card { background:rgba(30,41,59,0.8); padding:2rem; border-radius:20px;
        box-shadow:0 20px 40px -10px rgba(0,0,0,0.4); border:1px solid rgba(71,85,105,0.5);
        margin-bottom:2rem; backdrop-filter:blur(10px); transition:transform .3s ease; }
    .chart-card:hover { transform:translateY(-2px); border:1px solid rgba(139,92,246,0.3); }
    .chart-title { font-size:1.4rem; font-weight:600; color:#f8fafc;
        margin-bottom:1.5rem; border-bottom:2px solid rgba(139,92,246,0.3);
        padding-bottom:.8rem; }
    /* …plus all the selectbox, multiselect, slider, scrollbar, hide menus styles */
</style>
""", unsafe_allow_html=True)

# Helper to standardize Altair styling
def create_altair_chart(chart):
    return (chart
        .configure(background='transparent')
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor='#e2e8f0',
                        titleColor='#e2e8f0',
                        gridColor='rgba(71,85,105,0.3)',
                        domainColor='rgba(71,85,105,0.5)')
        .configure_legend(labelColor='#e2e8f0', titleColor='#e2e8f0')
        .configure_title(color='#f8fafc')
    )

# Sidebar: navigation + filters
with st.sidebar:
    tab = st.radio("Dashboard Sections", ["Description", "Charts"])
    st.markdown("---")
    st.subheader("Filter Options")
    selected_country = st.selectbox(
        'Select Country', ['All'] + sorted(df['Country'].dropna().unique())
    )
    selected_attack_types = st.multiselect(
        'Select Attack Type(s)', sorted(df['Attack Type'].dropna().unique())
    )
    st.subheader("Filter by Year Range")
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    selected_year_range = st.slider(
        "Select Year Range", min_year, max_year, (min_year, max_year), step=1
    )

# Apply filters
df_filtered = df[
    (df['Year'] >= selected_year_range[0]) &
    (df['Year'] <= selected_year_range[1])
].copy()
if selected_country != 'All':
    df_filtered = df_filtered[df_filtered['Country'] == selected_country]
if selected_attack_types:
    df_filtered = df_filtered[df_filtered['Attack Type'].isin(selected_attack_types)]

# Description Tab
if tab == "Description":
    st.title("Project Description")
    st.markdown("""

# 🛡️ Cybersecurity Analytics Dashboard

A modern interactive dashboard built with **Streamlit**, **Plotly**, and **Altair** to explore and analyze cybersecurity incidents across various countries, industries, and attack types. This tool allows users to **filter, visualize, and understand** patterns in historical cyber attack data — including severity, financial damage, defense effectiveness, and incident complexity.

---

## 🚀 Project Features

- **Interactive Filters:** Year range, country, and attack type filtering in sidebar
- **Smart Metrics:** Auto-calculates total incidents, affected users, and total financial loss
- **Critical Incidents Tagging:** Automatically flags attacks with >500K users affected and long resolution times
- **Severity Classification:** Tags incidents as `Low`, `Medium`, or `High` based on financial loss
- **Attack Complexity Categorization:** Classifies technical vs. social vulnerabilities
- **Visual Modules:**
  - Pie & Donut charts (severity, defense effectiveness, critical incidents)
  - Bar charts for attack type comparisons
  - Choropleth map (animated over years)
  - Sankey diagram showing attack flow (Source → Type → Industry)
  - Heatmap of dominant attack types per country and industry
  - Year-wise comparisons: Defense vs. Effectiveness / Severity

---

## 🧠 Insights Enabled

- Most vulnerable industries and countries
- Effectiveness of defense mechanisms over time
- Common attack vectors and attack sources
- Relationships between defense mechanisms and severity
- Data-driven identification of high-impact attacks

---

## 🗂️ File Structure

\`\`\`
├── cybersecurity_dashboard.py     # Main Streamlit application
├── cybersecurity_dataset.csv      # Primary dataset (must be in the same directory)
├── README.md                      # Project documentation (this file)
\`\`\`

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) – UI framework for rapid dashboard development
- [Pandas](https://pandas.pydata.org/) – Data manipulation and preprocessing
- [Plotly](https://plotly.com/) – Interactive charts and choropleths
- [Altair](https://altair-viz.github.io/) – Declarative statistical visualization
- [Matplotlib](https://matplotlib.org/) – Supplementary static plots
- CSS custom styling – for a modern, dark-themed UI

---

## 📊 Dataset Info

The dashboard expects a CSV file named `cybersecurity_dataset.csv` with the following columns (required):

- `Country`
- `Year`
- `Attack Type`
- `Security Vulnerability Type`
- `Defense Mechanism Used`
- `Attack Source`
- `Target Industry`
- `Financial Loss (in Million $)`
- `Number of Affected Users`
- `Incident Resolution Time (in Hours)`

---
                
### ✨ Additional Derived Columns Added to `cybersecurity_dataset`

The following columns were **not part of the original dataset**. They were created to enhance analysis, visualization, and model performance. Each column captures important aspects of cybersecurity incidents that are useful for dashboards, machine learning, or decision support.


| 🆕 Column Name             | 💡 Purpose & Insight                                                                                  |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| `Attack Complexity`       | Rates complexity (`Low`, `Medium`, `High`) based on the exploited vulnerability. Supports strategy development and threat modeling. |
| `Defense Effectiveness`   | Classifies resolution as `Effective` (≤ 24 hrs) or `Ineffective` (> 24 hrs). Useful for assessing the real-world performance of security tools. |
| `Attack Vector Type`      | Identifies if the attack vector is `Human` (e.g. Social Engineering) or `System` (e.g. Zero-day). Supports prevention strategy focus. |


    """)

elif tab == "Charts":
    st.markdown('<h1 class="main-header">Cybersecurity Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_incidents = len(df_filtered)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_incidents:,}</div>
            <div class="metric-label">Total Incidents</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_loss = df_filtered['Financial Loss (in Million $)'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_loss:.1f}M</div>
            <div class="metric-label">Total Financial Loss</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_users = df_filtered['Number of Affected Users'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_users:,.0f}</div>
            <div class="metric-label">Avg Affected Users</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        unique_countries = df_filtered['Country'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{unique_countries}</div>
            <div class="metric-label">Countries Affected</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # First Row of Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Defense Mechanisms by Attack Type</div>
        """, unsafe_allow_html=True)

        attack_options = df_filtered["Attack Type"].dropna().unique()
        selected_attack = st.selectbox("Select Attack Type", options=attack_options, key="defense_attack")
        attack_df = df_filtered[df_filtered["Attack Type"] == selected_attack]

        if not attack_df.empty:
            defense_counts = attack_df["Defense Mechanism Used"].value_counts().reset_index()
            defense_counts.columns = ["Defense Mechanism", "Count"]
            chart = alt.Chart(defense_counts).mark_bar().encode(
                x=alt.X("Defense Mechanism", sort='-y', axis=alt.Axis(labelAngle=-45)),
                y="Count",
                color=alt.Color("Defense Mechanism", scale=alt.Scale(scheme="category10")),
                tooltip=["Defense Mechanism", "Count"]
            ).properties(width=400, height=300)

            # Apply transparent background configuration
            chart = create_altair_chart(chart)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No data available for the selected attack type.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Severity Distribution</div>
        """, unsafe_allow_html=True)

        attack_selected = st.selectbox("Select Attack Type", df_filtered["Attack Type"].dropna().unique(), key="severity_attack")
        severity_df = df_filtered[df_filtered["Attack Type"] == attack_selected]["Severity"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)

        fig = go.Figure(data=[go.Pie(
            labels=severity_df.index,
            values=severity_df.values,
            hole=0.4,
            marker_colors=["#ef4444", "#f59e0b", "#10b981"],
            textinfo='label+percent',
            textposition='outside'
        )])
        fig.update_layout(
            height=300,
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Second Row of Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Average Affected Users by Attack Type</div>
        """, unsafe_allow_html=True)

        means = df_filtered.groupby("Attack Type")["Number of Affected Users"].mean().reset_index().sort_values(by="Number of Affected Users", ascending=False)
        chart2 = alt.Chart(means).mark_bar().encode(
            x=alt.X("Attack Type", sort='-y', axis=alt.Axis(labelAngle=-45)),
            y="Number of Affected Users",
            color=alt.Color("Attack Type", scale=alt.Scale(scheme="set1")),
            tooltip=["Attack Type", "Number of Affected Users"]
        ).properties(width=400, height=300)

        # Apply transparent background configuration
        chart2 = create_altair_chart(chart2)
        st.altair_chart(chart2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Attack Types by Industry</div>
        """, unsafe_allow_html=True)

        industry_options = df_filtered["Target Industry"].dropna().unique()
        selected_industry = st.selectbox("Choose Target Industry", industry_options)
        attack_counts = df_filtered[df_filtered["Target Industry"] == selected_industry]["Attack Type"].value_counts().reset_index()
        attack_counts.columns = ["Attack Type", "Count"]

        chart3 = alt.Chart(attack_counts).mark_bar().encode(
            x=alt.X("Attack Type", sort='-y', axis=alt.Axis(labelAngle=-45)),
            y="Count",
            color=alt.Color("Attack Type", scale=alt.Scale(scheme="set2")),
            tooltip=["Attack Type", "Count"]
        ).properties(width=400, height=300)

        # Apply transparent background configuration
        chart3 = create_altair_chart(chart3)
        st.altair_chart(chart3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Third Row - Full Width Charts
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Attack Types by Source</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        source_options = df_filtered["Attack Source"].dropna().unique()
        selected_source = st.selectbox("Select Attack Source", source_options)

    with col2:
        source_counts = df_filtered[df_filtered["Attack Source"] == selected_source]["Attack Type"].value_counts().reset_index()
        source_counts.columns = ["Attack Type", "Count"]
        chart5 = alt.Chart(source_counts).mark_bar().encode(
            x=alt.X("Attack Type:N", sort='-y', axis=alt.Axis(labelAngle=-45)),
            y="Count:Q",
            color=alt.Color("Attack Type:N", scale=alt.Scale(scheme="viridis")),
            tooltip=["Attack Type", "Count"]
        ).properties(width=700, height=300)

        # Apply transparent background configuration
        chart5 = create_altair_chart(chart5)
        st.altair_chart(chart5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Fourth Row - Financial Loss
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Total Financial Loss by Industry</div>
    """, unsafe_allow_html=True)

    loss_df = df_filtered.groupby("Target Industry")["Financial Loss (in Million $)"].sum().reset_index()
    loss_df = loss_df.sort_values("Financial Loss (in Million $)", ascending=True)

    chart6 = alt.Chart(loss_df).mark_bar().encode(
        x="Financial Loss (in Million $):Q",
        y=alt.Y("Target Industry:N", sort="-x"),
        color=alt.Color("Target Industry:N", scale=alt.Scale(scheme="plasma")),
        tooltip=["Target Industry", "Financial Loss (in Million $)"]
    ).properties(width=800, height=400)

    # Apply transparent background configuration
    chart6 = create_altair_chart(chart6)
    st.altair_chart(chart6, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- Contributed Visuals ---
    st.markdown('<h2 style="margin-top:2rem; color:#f8fafc;">Contributed Visuals</h2>', unsafe_allow_html=True)

    # 1. Heatmap: Top attack per (Country, Industry)
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Top Attack Type per Country & Industry</div>
    """, unsafe_allow_html=True)
    grouped = df_filtered.groupby(['Country', 'Target Industry', 'Attack Type']).size().reset_index(name='Count')
    most_common = grouped.sort_values('Count', ascending=False).drop_duplicates(['Country', 'Target Industry'])
    pivot = most_common.pivot(index='Country', columns='Target Industry', values='Attack Type')
    codes = pivot.apply(lambda col: pd.Categorical(col).codes)
    fig_heat = go.Figure(data=go.Heatmap(
        z=codes.values,
        x=codes.columns,
        y=codes.index,
        text=pivot.values,
        hoverinfo="text",
        colorscale='Blues'
    ))
    fig_heat.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0')
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Choropleth: Common attack type per country over time
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Most Common Attack Type by Country Over Time</div>
    """, unsafe_allow_html=True)
    attack_counts = df_filtered.groupby(['Year', 'Country', 'Attack Type']).size().reset_index(name='Count')
    top_attacks = attack_counts.sort_values('Count', ascending=False).drop_duplicates(['Year', 'Country'])
    impact = df_filtered.groupby(['Year', 'Country'])[['Financial Loss (in Million $)', 'Number of Affected Users']].sum().reset_index()
    impact.columns = ['Year', 'Country', 'Total Financial Loss', 'Total Affected Users']
    merged = pd.merge(top_attacks, impact, on=['Year', 'Country'], how='left')
    chor = px.choropleth(
        merged,
        locations='Country',
        locationmode='country names',
        color='Attack Type',
        animation_frame='Year',
        hover_name='Country',
        hover_data=['Total Financial Loss', 'Total Affected Users'],
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    chor.update_geos(showcoastlines=True, projection_type="natural earth")
    chor.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0')
    )
    st.plotly_chart(chor, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Sankey: Source → Type → Industry
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Attack Flow: Source → Type → Industry</div>
    """, unsafe_allow_html=True)
    df_sankey = df_filtered[['Attack Source', 'Attack Type', 'Target Industry']].dropna().copy()
    df_sankey = df_sankey[df_sankey['Attack Type'].isin(df_sankey['Attack Type'].value_counts().head(5).index)]
    labels = pd.unique(df_sankey[['Attack Source','Attack Type','Target Industry']].values.ravel())
    label_map = {label: idx for idx, label in enumerate(labels)}
    source = df_sankey['Attack Source'].map(label_map)
    target = df_sankey['Attack Type'].map(label_map)
    mid = df_sankey['Target Industry'].map(label_map)
    import collections
    link1 = collections.Counter(zip(source, target))
    link2 = collections.Counter(zip(target, mid))
    all_links = []
    for (s, t), v in link1.items(): all_links.append((s, t, v))
    for (s, t), v in link2.items(): all_links.append((s, t, v))
    sources, targets, values = zip(*all_links)
    sank_fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color='black', width=0.5), label=list(labels)),
        link=dict(source=list(sources), target=list(targets), value=list(values))
    )])
    sank_fig.update_layout(
        # Remove extra padding, title handled by card header
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0')
    )
    st.plotly_chart(sank_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Chart: Most common attack type by selected attack source
    st.markdown("""<div class='chart-card'>
    <div class='chart-title'>Most Common Attack Type by Source</div>""", unsafe_allow_html=True)

    source_input = st.selectbox("Choose an Attack Source", sorted(df_filtered['Attack Source'].dropna().unique()), key="chart_source_input")
    top_type = df_filtered[df_filtered['Attack Source'] == source_input]['Attack Type'].value_counts().idxmax()
    st.success(f"The most common attack done by **{source_input}** source is: **{top_type}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # CRITICAL INCIDENTS CHART - UPDATED TO PLOTLY VERSION
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Critical Incidents by Attack Type</div>
        """, unsafe_allow_html=True)

    if 'Critical' in df.columns:
        # Filter and count critical incidents
        critical_counts = df[df['Critical'] == True]['Attack Type'].value_counts()
        
        if not critical_counts.empty:
            # Create Plotly Donut Chart
            fig = go.Figure(
                data=[go.Pie(
                    labels=critical_counts.index,
                    values=critical_counts.values,
                    hole=0.4,
                    marker=dict(colors=px.colors.qualitative.Set3),
                    hoverinfo='label+percent+value',
                    textinfo='percent+label'
                )]
            )

            fig.update_layout(
                title_text='Critical Incidents by Attack Type',
                annotations=[dict(text='Critical', x=0.5, y=0.5, font_size=16, showarrow=False)],
                showlegend=True,
                margin=dict(t=60, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0')
            )

            # Show in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No critical incidents found.")
    else:
        st.warning("Column 'Critical' not found in dataset.")

    st.markdown("</div>", unsafe_allow_html=True)

    # DEFENSE EFFECTIVENESS - CONVERTED TO PLOTLY PIE CHART
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Defense Effectiveness</div>
        """, unsafe_allow_html=True)
    
    if 'Defense Effectiveness' in df.columns:
        # Count defense effectiveness values
        counts = df['Defense Effectiveness'].value_counts()

        # Create Plotly Pie Chart
        fig2 = px.pie(
            names=counts.index,
            values=counts.values,
            title='Defense Effectiveness',
            color_discrete_sequence=['#2ecc71', '#e74c3c'],
            hole=0  # Set to 0.5 for a donut
        )

        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=[0.05]*len(counts),  # Explode all slices slightly
            marker=dict(line=dict(color='black', width=1))
        )
        
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )

        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ATTACK TYPE VS SEVERITY - CONVERTED TO PLOTLY GROUPED BAR CHART
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Attack Type vs Severity</div>
        """, unsafe_allow_html=True)
    
    if 'Severity' in df.columns:
        # Pivot the table
        pivot = df.pivot_table(index='Attack Type', columns='Severity', aggfunc='size', fill_value=0).reset_index()

        # Melt for Plotly Express
        pivot_melted = pivot.melt(id_vars='Attack Type', var_name='Severity', value_name='Count')

        # Plotly grouped bar chart
        fig = px.bar(
            pivot_melted,
            x='Attack Type',
            y='Count',
            color='Severity',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set3,
            title='Attack Type vs Severity Level'
        )
        
        fig.update_layout(
            xaxis_tickangle=45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )

        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # DEFENSE MECHANISM VS EFFECTIVENESS BY YEAR - CONVERTED TO PLOTLY
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Defense Mechanism vs Effectiveness by Year</div>
        """, unsafe_allow_html=True)

    if 'Defense Effectiveness' in df.columns and 'Defense Mechanism Used' in df.columns and 'Year' in df.columns:
        years = sorted(df['Year'].unique())
        selected_year_eff = st.slider("Select Year for Defense Mechanism vs Effectiveness", 
                                      min_value=years[0], max_value=years[-1], 
                                      value=years[0], step=1, key='eff_year_slider')

        # Filter data for the selected year
        df_year_eff = df[df['Year'] == selected_year_eff]

        # Create pivot table: Defense Mechanism vs Defense Effectiveness counts
        pivot_eff = df_year_eff.pivot_table(index='Defense Mechanism Used', 
                                           columns='Defense Effectiveness',
                                           aggfunc='size', fill_value=0).reset_index()

        # Melt for Plotly
        pivot_melted = pivot_eff.melt(id_vars='Defense Mechanism Used', 
                                     var_name='Defense Effectiveness', 
                                     value_name='Number of Incidents')

        # Plotly grouped bar chart
        fig_eff = px.bar(
            pivot_melted,
            x='Defense Mechanism Used',
            y='Number of Incidents',
            color='Defense Effectiveness',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2,
            title=f'Defense Mechanism vs Effectiveness in {selected_year_eff}'
        )
        
        fig_eff.update_layout(
            xaxis_tickangle=45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )

        st.plotly_chart(fig_eff, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # DEFENSE MECHANISM VS SEVERITY BY YEAR - CONVERTED TO PLOTLY
    st.markdown("""
            <div class="chart-card">
                <div class="chart-title">Defense Mechanism vs Severity by Year</div>
            """, unsafe_allow_html=True)
    # IDEA 6: Defense Mechanism vs Severity by Year
    if 'Severity' in df.columns and 'Defense Mechanism Used' in df.columns and 'Year' in df.columns:
        years = sorted(df['Year'].unique())
        selected_year = st.slider("Select Year for Defense Mechanism vs Severity", min_value=years[0],
                                  max_value=years[-1], value=years[0], step=1)

        # Filter data for selected year
        df_year = df[df['Year'] == selected_year]

        # Create pivot table: Defense Mechanism vs Severity counts
        pivot_sev = df_year.pivot_table(index='Defense Mechanism Used', columns='Severity', aggfunc='size',
                                        fill_value=0)

        # Plot with matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        pivot_sev.plot(kind='bar', stacked=False, colormap='Set2', ax=ax)
        ax.set_title(f'Defense Mechanism vs Severity in {selected_year}')
        ax.set_xlabel('Defense Mechanism Used')
        ax.set_ylabel('Number of Incidents')
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
