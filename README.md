# 🏅 Olympics Analyzer

![Python Version](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-Educational-green)
![Streamlit](https://img.shields.io/badge/streamlit-v1.30-orange)

A **Streamlit-based interactive dashboard** for exploring Olympic Games data — including athletes, countries, sports, events, and medal trends over time.

---

## 🌟 Features

- Analyze **medal tallies** by year, country, or overall
- Visualize **overall statistics**: number of editions, sports, events, athletes, and nations
- Explore **country-wise performance** with top athletes and heatmaps
- Inspect **athlete-wise insights**: age, height vs weight, gold medal distribution, and gender participation
- Interactive **charts and heatmaps** with Plotly, Seaborn, and Matplotlib

---

## 🧠 How It Works

1. User selects an **analysis option** from the sidebar: Medal Tally, Overall Analysis, Country-wise Analysis, or Athlete-wise Analysis.
2. Data is preprocessed to include only **Summer Olympics** and merged with NOC-to-region mapping.
3. Visualizations and tables are dynamically generated based on **user selections**.
4. Users can explore trends over time, top athletes, country performance, and athlete demographics.

---

## ⚡ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/1588manjotsingh7b/Olympics-analyzer.git
cd Olympics-analyzer
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run appp.py
```

---

## 🛠 Dependencies
- Python 3.x
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn

---

## 📦 Dataset
- athlete_events.csv — Contains athlete-level event results
- noc_regions.csv — Maps National Olympic Committees (NOCs) to countries/regions Datasets can be found in the /data folder (or specify the source if downloaded externally).

---

## 📜 License
- Educational / Personal Project

---

## 🎨 Optional Enhancements
- Add Winter Olympics data support
- Include medal prediction models for future games
- Add more interactive visualizations and filters
