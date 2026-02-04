# 🎬 Film Performance Analysis: Streaming vs. Theatrical (2019-2024)

**Interactive Tableau Dashboard analyzing 530 films to optimize release strategy and budget allocation decisions**

[![View Dashboard](https://img.shields.io/badge/Tableau-Public-blue?style=for-the-badge&logo=tableau)](https://public.tableau.com/app/profile/alexandra.lugo/viz/streaming-vs-theatrical-analytics/Dashboard)

---

## 📊 Live Dashboard

**[➡️ View Interactive Dashboard on Tableau Public](https://public.tableau.com/app/profile/alexandra.lugo/viz/streaming-vs-theatrical-analytics/Dashboard)**

![Dashboard Preview](images/dashboard_preview.png)

---

## 🎯 Project Overview

### Business Question
**Which film genres generate the highest ROI on streaming platforms vs. theatrical releases, and what budget ranges optimize platform-specific performance?**

### Key Findings

1. **🎬 Action Films: Theatrical-Only Champions**
   - Achieve 2,437% ROI when kept theatrical-only
   - Recommendation: Maintain 90-120 day theatrical exclusivity windows

2. **💰 Low Budgets Optimize Streaming ROI**
   - Films under $10M deliver 400-2,400% ROI across streaming platforms
   - Exception: Disney+ optimizes at medium budgets ($10M-$50M) for family content

3. **🎯 Crime Films: Streaming Superstars**
   - Gain 582% higher ROI when released to streaming after theatrical run
   - Recommendation: Pursue rapid streaming deals (30-45 day windows)

### Strategic Implications
This analysis could inform release windowing strategies worth **$10-50M per film** for major studios, suggesting genre-specific approaches rather than one-size-fits-all strategies.

---

## 🛠️ Technical Stack

### Data Collection & Processing
- **Python** (Pandas, Requests, NumPy)
- **TMDb API** - Movie data collection (budget, revenue, streaming availability)
- **SQLite** - Data storage and querying

### Analysis & Visualization
- **SQL** - Complex queries for dashboard metrics
- **Tableau Public** - Interactive dashboard
- **Jupyter Notebooks** - Exploratory data analysis

### Version Control
- **Git/GitHub** - Project management and documentation

---

## 📁 Project Structure
```
streaming-vs-theatrical-analytics/
│
├── data/
│   ├── raw/                              # Raw data from TMDb API
│   │   ├── theatrical_data_raw.csv
│   │   └── theatrical_streaming_combined.csv
│   ├── cleaned/                          # Processed, analysis-ready data
│   │   └── movies_final_dataset.csv
│   └── tableau/                          # Data extracts for Tableau
│       ├── movies_full_data.csv
│       ├── roi_by_genre_strategy.csv
│       └── streaming_boost.csv
│
├── notebooks/                            # Jupyter notebooks
│   ├── 02_exploratory_analysis.ipynb
│   └── KEY_FINDINGS.md
│
├── scripts/                              # Python data pipeline
│   ├── test_api_connection.py
│   ├── collect_theatrical_data.py
│   ├── add_streaming_data.py
│   ├── clean_and_engineer_features.py
│   └── export_data_for_tableau.py
│
├── sql/                                  # SQL queries
│   └── dashboard_queries.sql
│
├── images/                               # Visualizations & screenshots
│   ├── dashboard_preview.png
│   ├── roi_by_genre_strategy.png
│   └── streaming_boost_by_genre.png
│
├── .env.example                          # API key template
├── .gitignore                            # Git ignore file
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- TMDb API Key ([Get one here](https://www.themoviedb.org/settings/api))
- Tableau Public (free download)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/alexandranlugo/streaming-vs-theatrical-analytics.git
cd streaming-vs-theatrical-analytics
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API key**
```bash
cp .env.example .env
# Add your TMDb API key to .env
```

4. **Run the data collection pipeline**
```bash
# Test API connection
python scripts/test_api_connection.py

# Collect theatrical data (2019-2024)
python scripts/collect_theatrical_data.py

# Enrich with streaming availability data
python scripts/add_streaming_data.py

# Clean and engineer features
python scripts/clean_and_engineer_features.py

# Export for Tableau
python scripts/export_data_for_tableau.py
```

5. **View the dashboard**
- [View live dashboard on Tableau Public](https://public.tableau.com/app/profile/alexandra.lugo/viz/streaming-vs-theatrical-analytics/Dashboard)
- Or open Tableau Public and connect to `data/tableau/movies_full_data.csv`

---

## 📈 Methodology

### Data Collection
- **Source:** TMDb (The Movie Database) API
- **Scope:** 530 films released 2019-2024
- **Filters:** English-language films with budget & revenue data >$1K
- **Streaming Data:** Official platform availability (Netflix, Prime, Disney+, Hulu, HBO Max)

### Feature Engineering
Created 13 derived features including:
- `roi`: (Revenue - Budget) / Budget × 100
- `budget_category`: Low/Medium/High/Blockbuster tiers
- `release_strategy`: Theatrical Only / Theatrical → Streaming / Streaming-First
- `streaming_availability_score`: Platform count (0-5)
- `genre_consolidated`: Grouped similar genres

### Analysis Approach
1. **ROI by Genre & Strategy:** Compared average ROI across 18 genres and 4 release strategies
2. **Budget Optimization:** Analyzed optimal budget ranges per streaming platform
3. **Streaming Boost:** Calculated ROI difference (Theatrical → Streaming vs. Theatrical-Only)
4. **Trend Analysis:** Tracked performance changes (2019-2024)

---

## 📊 Key Visualizations

### ROI by Genre and Release Strategy
Compares performance across genres and strategies to identify optimal combinations. Action films in theatrical-only release show 2,437% ROI, while Crime films gain 582% from streaming.

### Budget Optimization by Platform
Low-budget films (<$10M) deliver highest ROI on Netflix (444%), Prime (2,433%), and Hulu (604%). Disney+ uniquely optimizes at medium budgets ($10M-$50M) with 866% ROI.

### Streaming Impact Analysis
Reveals which genres benefit from streaming release (Crime: +582%) vs. theatrical-only (Action: -1,934%).

### Historical Trends (2019-2024)
Tracks ROI evolution showing theatrical-only strategies maintain higher returns, with notable volatility during COVID-19 period (2020-2021).

---

## 🎤 Interview Soundbite

> "I built an end-to-end analytics pipeline analyzing 530 films from 2019-2024 using Python and the TMDb API. I discovered that Action films achieve 2,437% ROI when kept theatrical-only, while Crime films gain 582% higher ROI from rapid streaming releases. I translated these findings into an interactive Tableau dashboard that could inform release windowing strategies worth $10-50M per film for major studios."

---

## 📚 Data Sources

- [The Movie Database (TMDb) API](https://www.themoviedb.org/documentation/api) - Movie metadata, financial data, streaming availability

---

## 🤝 Connect

**Alexandra Lugo**  
Data Science @ NYU Stern '26  

- 🌐 Portfolio: [alexandralugo.com](https://alexandralugo.com)
- 💼 LinkedIn: [linkedin.com/in/lugoalexandra](https://www.linkedin.com/in/lugoalexandra/)
- 💻 GitHub: [@alexandranlugo](https://github.com/alexandranlugo)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- TMDb for providing free API access
- NYU Stern for resources and support
- Anthropic's Claude for project guidance

---

**⭐ If you found this project helpful, please consider starring the repository!**
