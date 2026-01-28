# Streaming vs. Theatrical Film Performance Analytics

**Analyzing which film genres succeed on streaming platforms vs. theatrical releases**

[![Tableau Public](https://img.shields.io/badge/Tableau-Public-blue)](LINK_COMING_SOON)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project Overview

**Business Question:**  
*Which film genres generate higher ROI on streaming platforms vs. theatrical releases, and what drives platform-specific success?*

This project analyzes 500-1000 films (2019-2024) to uncover strategic insights for content acquisition, production decisions, and release strategy planning at media companies like Netflix, Amazon Studios, and traditional film studios.

---

## Key Findings

> **Project in Progress** - Findings will be updated by [DATE]

1. [Key Insight #1]
2. [Key Insight #2]
3. [Key Insight #3]

---

## Tech Stack

- **Data Collection:** Python (requests, TMDb API)
- **Data Processing:** Pandas, NumPy
- **Database:** SQL (SQLite)
- **Visualization:** Tableau Public
- **Version Control:** Git/GitHub

---

## Project Structure
```
├── data/
│   ├── raw/              # Original API responses & Kaggle datasets
│   └── cleaned/          # Processed data ready for analysis
├── notebooks/            # Jupyter notebooks for exploration
├── scripts/              # Python scripts for data pipeline
├── sql/                  # SQL queries for analysis
├── images/               # Dashboard screenshots
└── requirements.txt      # Python dependencies
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- TMDb API Key ([Get one here](https://www.themoviedb.org/settings/api))
- Tableau Public (free)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alexandranlugo/streaming-vs-theatrical-analytics.git
cd streaming-vs-theatrical-analytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Add your TMDb API key to .env
```

4. Run the data collection script:
```bash
python scripts/collect_data.py
```

---

## Interactive Dashboard

> **Coming Soon:** Embedded Tableau Public dashboard

[View Live Dashboard](#) | [Download Workbook](#)

![Dashboard Preview](images/dashboard_preview.png)

---

## Data Sources

- [The Movie Database (TMDb) API](https://www.themoviedb.org/documentation/api)
- [Kaggle: Netflix Movies & TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- [Kaggle: IMDB Movies Dataset](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)

---

## Methodology

1. **Data Collection:** Extract film data from TMDb API and Kaggle datasets
2. **Data Cleaning:** Handle missing values, standardize genres, engineer features (ROI, platform categorization)
3. **Analysis:** SQL queries to compare performance metrics across platforms and genres
4. **Visualization:** Interactive Tableau dashboard with filters and drill-downs
5. **Insights:** Identify strategic recommendations for content decision-makers

---

## 📬 Contact

**Alexandra Lugo**  
Data Scientist | NYU '26  
[Portfolio](https://alexandralugo.com)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- TMDb for providing free API access
- Kaggle community for datasets