
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

## 🧪 How to Run

1. **Install dependencies**
\`\`\`bash
pip install streamlit pandas plotly altair matplotlib
\`\`\`

2. **Place your dataset**
Make sure `cybersecurity_dataset.csv` is in the root directory.

3. **Run the app**
\`\`\`bash
streamlit run cybersecurity_dashboard.py
\`\`\`

---
